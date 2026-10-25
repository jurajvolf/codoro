from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import hashlib
import secrets
import re
from .models import User, SchoolClass, SubscriptionLicense, SchoolLicenseRequest, PasswordHistory
from .security import (
    is_rate_limited,
    reset_rate_limit,
    check_honeypot,
    safe_int,
    sanitize_text,
    safe_redirect_url,
)
from gamification.models import DorosTransaction, Badge, StudentBadge
from gamification.services import get_student_stats, award_badges, ensure_badges_exist


def evaluate_password_strength(password):
    """
    Vyhodnotí silu hesla na 3 úrovne:
    1: Slabé (nespĺňa dĺžku 8 alebo málo kritérií)
    2: Stredné (dĺžka 8+ a spĺňa časť kritérií)
    3: Silné (dĺžka 8+, veľké aj malé písmená, aspoň 1 číslo, aspoň 1 špeciálny znak)
    Používateľa pustí do registrácie / zmeny hesla iba pri úrovni 3 (Silné).
    """
    if not password:
        return 1, False, ["Zadaj heslo."], ["Please enter a password."]

    has_len = len(password) >= 8
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?~`]', password))

    errors_sk = []
    errors_en = []
    if not has_len:
        errors_sk.append("Heslo musí mať aspoň 8 znakov.")
        errors_en.append("Password must be at least 8 characters long.")
    if not (has_upper and has_lower):
        errors_sk.append("Heslo musí obsahovať veľké aj malé písmená.")
        errors_en.append("Password must contain both uppercase and lowercase letters.")
    if not has_digit:
        errors_sk.append("Heslo musí obsahovať aspoň jednu číslicu (0–9).")
        errors_en.append("Password must contain at least one digit (0–9).")
    if not has_special:
        errors_sk.append("Heslo musí obsahovať aspoň jeden špeciálny znak (!@#$%...).")
        errors_en.append("Password must contain at least one special character (!@#$%...).")

    components_met = sum([has_upper and has_lower, has_digit, has_special])

    if has_len and components_met == 3:
        level = 3
        is_strong = True
    elif has_len or components_met >= 2:
        level = 2
        is_strong = False
    else:
        level = 1
        is_strong = False

    return level, is_strong, errors_sk, errors_en


def generate_unique_join_code(base_name="CLASS"):
    """Vygeneruje unikátny, zapamätateľný kód triedy (napr. IVC-2027 alebo PY-789A)."""
    clean = re.sub(r'[^A-Za-z0-9]', '', base_name).upper()[:4] or "CLASS"
    year = timezone.now().year
    code = f"{clean}-{year}"
    if not SchoolClass.objects.filter(join_code=code).exists():
        return code
    for _ in range(30):
        suffix = secrets.token_hex(2).upper()
        cand = f"{clean}-{suffix}"
        if not SchoolClass.objects.filter(join_code=cand).exists():
            return cand
    return f"C-{secrets.token_hex(3).upper()}"


def get_active_lang(request):
    if request.user.is_authenticated:
        return request.user.preferred_language
    return request.session.get('ui_lang', 'sk')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    lang = get_active_lang(request)
    if request.method == 'POST':
        if not check_honeypot(request):
            err = "Bot activity detected." if lang == 'en' else "Zistená automatizovaná aktivita."
            messages.error(request, err)
            return render(request, 'accounts/login.html', {'ui_lang': lang})

        username = sanitize_text(request.POST.get('username', ''), max_length=150)
        password = request.POST.get('password', '')

        if is_rate_limited(request, 'login', limit=10, window_seconds=300, identifier=username.lower()):
            err = (
                "Too many login attempts. Please wait a few minutes and try again."
                if lang == 'en'
                else "Príliš veľa neúspešných pokusov o prihlásenie. Počkaj prosím pár minút a skús to znova."
            )
            messages.error(request, err)
            return render(request, 'accounts/login.html', {'ui_lang': lang}, status=429)

        user = authenticate(request, username=username, password=password)
        if user:
            reset_rate_limit(request, 'login', identifier=username.lower())
            if 'ui_lang' in request.session:
                user.preferred_language = request.session['ui_lang']
                user.save(update_fields=['preferred_language'])
            login(request, user)
            return redirect('dashboard')

        err = "Invalid username or password." if lang == 'en' else "Nesprávne používateľské meno alebo heslo."
        messages.error(request, err)

    return render(request, 'accounts/login.html', {'ui_lang': lang})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    lang = get_active_lang(request)
    initial_tab = request.GET.get('role', 'student')

    if request.method == 'POST':
        account_type = (request.POST.get('account_type') or request.POST.get('role') or 'student').lower()
        pref_lang = request.POST.get('preferred_language', lang)
        if pref_lang not in ('sk', 'en'):
            pref_lang = lang

        if not check_honeypot(request):
            err = "Bot activity detected." if pref_lang == 'en' else "Zistená automatizovaná aktivita."
            messages.error(request, err)
            return render(request, 'accounts/register.html', {'ui_lang': lang, 'active_tab': account_type})

        if is_rate_limited(request, 'register', limit=12, window_seconds=600):
            err = (
                "Too many registration attempts. Please try again later."
                if pref_lang == 'en'
                else "Príliš veľa pokusov o registráciu. Skús to prosím o chvíľu."
            )
            messages.error(request, err)
            return render(request, 'accounts/register.html', {'ui_lang': lang, 'active_tab': account_type}, status=429)

        username = sanitize_text(request.POST.get('username', ''), max_length=150)
        email = sanitize_text(request.POST.get('email', ''), max_length=254)
        first_name = sanitize_text(request.POST.get('first_name', ''), max_length=150)
        last_name = sanitize_text(request.POST.get('last_name', ''), max_length=150)
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "Vyplň používateľské meno a heslo." if pref_lang == 'sk' else "Please fill in username and password.")
            return render(request, 'accounts/register.html', {'ui_lang': lang, 'active_tab': account_type})

        level, is_strong, errs_sk, errs_en = evaluate_password_strength(password)
        if not is_strong:
            err = " ".join(errs_en) if pref_lang == 'en' else " ".join(errs_sk)
            messages.error(request, err)
            return render(request, 'accounts/register.html', {'ui_lang': lang, 'active_tab': account_type})

        if User.objects.filter(username=username).exists():
            err = "This username is already taken." if pref_lang == 'en' else "Toto používateľské meno sa už používa."
            messages.error(request, err)
            return render(request, 'accounts/register.html', {'ui_lang': lang, 'active_tab': account_type})

        # ==========================================================
        # A) REGISTRÁCIA UČITEĽA (TEACHER & SCHOOL ECOSYSTEM)
        # ==========================================================
        if account_type == 'teacher':
            license_code = sanitize_text(request.POST.get('teacher_license_code') or request.POST.get('school_license_key') or '', max_length=64).upper()
            initial_class_name = sanitize_text(request.POST.get('initial_class_name', ''), max_length=100)

            lic = None
            if license_code:
                lic = SubscriptionLicense.objects.filter(code=license_code, is_active=True).first()
                if not lic or lic.current_uses >= lic.max_uses:
                    err = (
                        "Invalid or exhausted school license key. Please check your key or request a pilot key."
                        if pref_lang == 'en'
                        else "Zadaný školský licenčný kľúč je neplatný alebo vyčerpaný. Môžete požiadať o pilotný kľúč."
                    )
                    messages.error(request, err)
                    return render(request, 'accounts/register.html', {'ui_lang': lang, 'active_tab': 'teacher'})
                lic.current_uses += 1
                lic.save(update_fields=['current_uses'])
            else:
                # Automatické vydanie pilotnej školskej EDU licencie (35 žiakov)
                pilot_code = f"EDU-PILOT-{secrets.token_hex(3).upper()}"
                lic = SubscriptionLicense.objects.create(
                    code=pilot_code,
                    tier=User.SubscriptionTier.EDU,
                    max_uses=35,
                    current_uses=1,
                    is_active=True
                )
                SchoolLicenseRequest.objects.create(
                    school_name=f"Škola - {first_name} {last_name}",
                    contact_name=f"{first_name} {last_name}",
                    email=email,
                    estimated_students=35,
                    note="Automaticky aktivovaný pilotný prístup pri registrácii učiteľa",
                    status=SchoolLicenseRequest.Status.APPROVED,
                    generated_license=lic
                )

            teacher_user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role=User.Role.TEACHER,
                subscription_tier=User.SubscriptionTier.EDU,
                is_staff=True,
                preferred_language=pref_lang,
                doros=1000,
                avatar='wizard',
                avatar_color='indigo'
            )
            PasswordHistory.objects.create(user=teacher_user, password_hash=teacher_user.password)

            created_class = None
            if initial_class_name:
                code = generate_unique_join_code(initial_class_name)
                created_class = SchoolClass.objects.create(
                    name=initial_class_name,
                    join_code=code,
                    teacher=teacher_user
                )

            request.session['ui_lang'] = pref_lang
            login(request, teacher_user)

            if created_class:
                msg = (
                    f"Welcome to Codoro Teacher Studio! Class '{created_class.name}' created with join code: {created_class.join_code}"
                    if pref_lang == 'en'
                    else f"Vitajte v Učiteľskom štúdiu Codoro! Trieda '{created_class.name}' bola vytvorená s kódom: {created_class.join_code}"
                )
            else:
                msg = (
                    "Welcome to Codoro Teacher Studio! You can now create your school classes."
                    if pref_lang == 'en'
                    else "Vitajte v Učiteľskom štúdiu Codoro! Môžete začať vytvárať svoje školské triedy."
                )
            messages.success(request, msg)
            return redirect('teacher_dashboard')

        # ==========================================================
        # B) REGISTRÁCIA ŠTUDENTA (STUDENT)
        # ==========================================================
        join_code = sanitize_text(request.POST.get('join_code') or request.POST.get('class_code') or '', max_length=32).upper()
        school_class = None
        if join_code:
            school_class = SchoolClass.objects.filter(join_code=join_code).first()
            if not school_class:
                warn = (
                    "Class code not found. Account created without a class."
                    if pref_lang == 'en'
                    else "Zadaný kód triedy neexistuje. Účet bol vytvorený bez priradenej triedy."
                )
                messages.warning(request, warn)

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=User.Role.STUDENT,
            school_class=school_class,
            preferred_language=pref_lang,
            doros=100
        )
        PasswordHistory.objects.create(user=user, password_hash=user.password)
        DorosTransaction.objects.create(
            student=user,
            amount=100,
            reason_sk="Uvítací bonus za registráciu do Codoro",
            reason_en="Welcome bonus for joining Codoro"
        )
        request.session['ui_lang'] = pref_lang
        login(request, user)
        msg = (
            "Welcome to Codoro! You received 100 starter Doros."
            if pref_lang == 'en'
            else "Vitaj v Codoro! Získal si štartovacích 100 Doros."
        )
        messages.success(request, msg)
        return redirect('dashboard')

    return render(request, 'accounts/register.html', {
        'ui_lang': lang,
        'active_tab': initial_tab
    })


def get_license_view(request):
    """
    Verejný portál pre školy a učiteľov na zaobstaranie školskej licencie Codoro EDU.
    Umožní okamžite získať pilotný kľúč a odoslať oficiálnu žiadosť.
    """
    lang = get_active_lang(request)

    if request.method == 'POST':
        if not check_honeypot(request):
            err = "Bot activity detected." if lang == 'en' else "Zistená automatizovaná aktivita."
            messages.error(request, err)
            return render(request, 'accounts/get_license.html', {'ui_lang': lang})

        if is_rate_limited(request, 'get_license', limit=8, window_seconds=600):
            err = (
                "Too many license requests. Please try again in a few minutes."
                if lang == 'en'
                else "Príliš veľa žiadostí o licenciu. Skúste to prosím o niekoľko minút."
            )
            messages.error(request, err)
            return render(request, 'accounts/get_license.html', {'ui_lang': lang}, status=429)

        school_name = sanitize_text(request.POST.get('school_name', ''), max_length=200)
        contact_name = sanitize_text(request.POST.get('contact_name') or request.POST.get('contact_person') or '', max_length=150)
        email = sanitize_text(request.POST.get('email', ''), max_length=254)
        phone = sanitize_text(request.POST.get('phone', ''), max_length=40)
        estimated_students = safe_int(
            request.POST.get('estimated_students') or request.POST.get('expected_students'),
            default=30,
            min_val=1,
            max_val=5000,
        )
        note = sanitize_text(request.POST.get('note', ''), max_length=1000)

        if not school_name or not contact_name or not email:
            messages.error(request, "Vyplňte prosím všetky povinné polia (škola, vyučujúci, e-mail).")
            return render(request, 'accounts/get_license.html', {'ui_lang': lang})

        # Okamžité vygenerovanie pilotného kľúča
        clean_prefix = re.sub(r'[^A-Za-z0-9]', '', school_name).upper()[:4] or "EDU"
        pilot_code = f"EDU-{clean_prefix}-{secrets.token_hex(3).upper()}"
        lic = SubscriptionLicense.objects.create(
            code=pilot_code,
            tier=User.SubscriptionTier.EDU,
            max_uses=max(10, estimated_students + 5),
            current_uses=0,
            is_active=True
        )

        SchoolLicenseRequest.objects.create(
            school_name=school_name,
            contact_name=contact_name,
            email=email,
            phone=phone,
            estimated_students=estimated_students,
            note=note,
            status=SchoolLicenseRequest.Status.PENDING,
            generated_license=lic
        )

        success_msg = (
            f"License key {lic.code} has been generated for {school_name}! You can now use it to register your teacher account."
            if lang == 'en'
            else f"Školský licenčný kľúč {lic.code} bol vygenerovaný pre {school_name}! Môžete ho ihneď použiť pri registrácii učiteľa."
        )
        messages.success(request, success_msg)

        return render(request, 'accounts/get_license.html', {
            'ui_lang': lang,
            'generated_license': lic,
            'school_name': school_name,
            'contact_name': contact_name,
        })

    return render(request, 'accounts/get_license.html', {'ui_lang': lang})


@login_required
def logout_view(request):
    lang = request.user.preferred_language
    logout(request)
    request.session['ui_lang'] = lang
    return redirect('login')


def switch_language(request, lang_code):
    """Prepne jazyk rozhrania pre prihláseného aj neprihláseného používateľa."""
    clean_code = (lang_code or '').strip().lower()
    if clean_code in ['sk', 'en']:
        request.session['ui_lang'] = clean_code
        request.session.modified = True
        try:
            request.session.save()
        except Exception:
            pass

        if request.user.is_authenticated:
            request.user.preferred_language = clean_code
            request.user.save(update_fields=['preferred_language'])

    # 1. Parameter ?next= má najvyššiu prioritu (chránené proti Open Redirect)
    raw_next = request.GET.get('next')
    next_url = safe_redirect_url(request, raw_next, fallback=None) if raw_next else None
    if not next_url:
        referer = request.META.get('HTTP_REFERER')
        if referer and '/lang/' not in referer:
            next_url = safe_redirect_url(request, referer, fallback=None)

    fallback = 'dashboard' if request.user.is_authenticated else 'landing_page'
    response = redirect(next_url or fallback)

    if clean_code in ['sk', 'en']:
        # path='/' je kritické, aby cookie platila pre celú doménu a všetky podstránky!
        response.set_cookie('codoro_lang', clean_code, max_age=60*60*24*365, path='/', samesite='Lax')

    return response


@login_required
@transaction.atomic
def repair_streak(request):
    user = request.user
    lang = user.preferred_language
    repair_cost = 200

    if user.lost_streak_value <= 0:
        msg = "You have no expired streak to restore." if lang == 'en' else "Nemáš žiadnu prerušenú sériu na obnovenie."
        messages.info(request, msg)
        return redirect('dashboard')

    if user.doros < repair_cost:
        msg = (
            f"You need {repair_cost} Doros to restore your streak."
            if lang == 'en'
            else f"Na obnovenie série potrebuješ {repair_cost} Doros."
        )
        messages.error(request, msg)
        return redirect('dashboard')

    user.doros -= repair_cost
    user.current_streak = user.lost_streak_value
    user.lost_streak_value = 0
    user.streak_lost_at = None
    user.save()

    DorosTransaction.objects.create(
        student=user,
        amount=-repair_cost,
        reason_sk=f"Obnovenie {user.current_streak}-dňovej série (Streak)",
        reason_en=f"Restored {user.current_streak}-day Streak"
    )
    msg = (
        f"Your {user.current_streak}-day streak has been restored!"
        if lang == 'en'
        else f"Tvoja {user.current_streak}-dňová séria bola úspešne obnovená!"
    )
    messages.success(request, msg)
    return redirect('dashboard')


@login_required
@transaction.atomic
def activate_license(request):
    if request.method == 'POST':
        lang = request.user.preferred_language
        if is_rate_limited(request, 'activate_license', limit=10, window_seconds=300, identifier=str(request.user.id)):
            err = "Too many license activation attempts. Please wait." if lang == 'en' else "Príliš veľa pokusov o aktiváciu licencie. Počkaj prosím chvíľu."
            messages.error(request, err)
            return redirect('shop')

        code = sanitize_text(request.POST.get('license_code', ''), max_length=64).upper()
        lic = SubscriptionLicense.objects.select_for_update().filter(code=code, is_active=True).first()

        if not lic or lic.current_uses >= lic.max_uses:
            err = "Invalid or exhausted license key." if lang == 'en' else "Neplatný alebo vyčerpaný licenčný kľúč."
            messages.error(request, err)
            return redirect('shop')

        request.user.subscription_tier = lic.tier
        request.user.save(update_fields=['subscription_tier'])
        lic.current_uses += 1
        lic.save(update_fields=['current_uses'])

        msg = (
            f"License {code} activated! You now have full access to PRO/EDU modules and unlimited AI tutor Codo."
            if lang == 'en'
            else f"Licencia {code} bola aktivovaná! Máš plný prístup k PRO/EDU obsahu a neobmedzenému AI tútorovi Codo."
        )
        messages.success(request, msg)
    return redirect('shop')


@login_required
def profile_view(request):
    """Podstránka Môj Profil, nastavenia avatara, zmena hesla a vitrína odznakov."""
    user = request.user
    lang = user.preferred_language

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_avatar':
            avatar = request.POST.get('avatar')
            avatar_color = request.POST.get('avatar_color')
            valid_avatars = dict(User.AVATAR_CHOICES)
            valid_colors = dict(User.AVATAR_COLORS)

            if avatar in valid_avatars:
                user.avatar = avatar
                if avatar_color and avatar_color in valid_colors:
                    user.avatar_color = avatar_color
                user.save(update_fields=['avatar', 'avatar_color'])
                msg = "Avatar updated successfully!" if lang == 'en' else "Profilový avatar bol úspešne zmenený!"
                messages.success(request, msg)

        elif action == 'update_info':
            first_name = sanitize_text(request.POST.get('first_name', ''), max_length=150)
            last_name = sanitize_text(request.POST.get('last_name', ''), max_length=150)
            preferred_language = request.POST.get('preferred_language', 'sk')
            if preferred_language in ['sk', 'en']:
                user.preferred_language = preferred_language
            user.first_name = first_name
            user.last_name = last_name
            user.save(update_fields=['first_name', 'last_name', 'preferred_language'])
            msg = "Profile information updated!" if lang == 'en' else "Informácie profilu boli aktualizované!"
            messages.success(request, msg)

        elif action == 'change_password':
            old_pass = request.POST.get('old_password', '')
            new_pass = request.POST.get('new_password', '')
            confirm_pass = request.POST.get('confirm_password', '')

            level, is_strong, errs_sk, errs_en = evaluate_password_strength(new_pass)

            if not user.check_password(old_pass):
                err = "Current password is not correct." if lang == 'en' else "Pôvodné heslo nie je správne."
                messages.error(request, err)
            elif not is_strong:
                err = " ".join(errs_en) if lang == 'en' else " ".join(errs_sk)
                messages.error(request, err)
            elif new_pass != confirm_pass:
                err = "New passwords do not match." if lang == 'en' else "Nové heslá sa nezhodujú."
                messages.error(request, err)
            elif user.is_password_in_history(new_pass):
                err = (
                    "New password cannot be the same as your current or any of your last 3 previous passwords."
                    if lang == 'en'
                    else "Nové heslo sa nesmie zhodovať s aktuálnym ani so žiadnym z tvojich posledných 3 predchádzajúcich hesiel."
                )
                messages.error(request, err)
            else:
                user.record_password_change(new_pass)
                update_session_auth_hash(request, user)
                msg = "Password changed successfully!" if lang == 'en' else "Heslo bolo úspešne zmenené!"
                messages.success(request, msg)

        return redirect('profile')

    # Skontrolujeme a udelíme prípadné nové odznaky
    award_badges(user)
    ensure_badges_exist()

    stats = get_student_stats(user)
    all_badges = Badge.objects.all().order_by('order')
    student_badges = {sb.badge_id: sb for sb in StudentBadge.objects.filter(student=user).select_related('badge')}

    # Zostavíme zoznam odznakov so stavom získania
    badge_list = []
    for b in all_badges:
        sb = student_badges.get(b.id)
        badge_list.append({
            'badge': b,
            'is_earned': sb is not None,
            'earned_at': sb.earned_at if sb else None,
        })

    return render(request, 'accounts/profile.html', {
        'stats': stats,
        'badge_list': badge_list,
        'earned_count': len(student_badges),
        'total_badges_count': all_badges.count(),
        'avatar_choices': User.AVATAR_CHOICES,
        'avatar_colors': User.AVATAR_COLORS,
        'illustrated_avatars': [
            {'code': 'student_alex', 'name_sk': 'Alex (Programátor)', 'name_en': 'Alex (Coder)', 'img_url': '/static/img/avatars/student_alex.jpg', 'desc_sk': 'Zvedavý Python študent s odhodlaním vyriešiť každý bug', 'desc_en': 'Curious Python coder ready to squash every bug'},
            {'code': 'student_mia', 'name_sk': 'Mia (Data Scientist)', 'name_en': 'Mia (Data Scientist)', 'img_url': '/static/img/avatars/student_mia.jpg', 'desc_sk': 'Milovníčka dátových štruktúr a analýzy algoritmov', 'desc_en': 'Lover of data structures and algorithmic efficiency'},
            {'code': 'student_sam', 'name_sk': 'Sam (Full-stack)', 'name_en': 'Sam (Full-stack)', 'img_url': '/static/img/avatars/student_sam.jpg', 'desc_sk': 'Architekt moderných webov a backend logiky', 'desc_en': 'Architect of modern web and backend logic'},
            {'code': 'cyber_ninja', 'name_sk': 'Cyber Ninja', 'name_en': 'Cyber Ninja', 'img_url': '/static/img/avatars/cyber_ninja.jpg', 'desc_sk': 'Expert na kryptografiu, bezpečnosť a čistý kód', 'desc_en': 'Expert in cryptography, security, and clean code'},
            {'code': 'codo', 'name_sk': 'Codo (AI Maskot)', 'name_en': 'Codo (AI Mascot)', 'img_url': '/static/img/avatars/codo.png', 'desc_sk': 'Priateľský spoločník a Sokratovský AI tútor', 'desc_en': 'Friendly guide and Socratic AI tutor'},
        ],
    })


@login_required
def certificate_view(request):
    """Oficiálny digitálny a tlačiteľný certifikát o absolvovaní kurzu Pythonu."""
    user = request.user
    stats = get_student_stats(user)
    today = timezone.localdate()

    # Unikátny overovací kód certifikátu odvodený od ID a dátumu
    hash_seed = f"codoro-cert-{user.id}-{user.username}-{user.level}"
    cert_hash = hashlib.sha256(hash_seed.encode('utf-8')).hexdigest()[:10].upper()
    cert_code = f"CDR-CERT-{user.id:04d}-{cert_hash}"

    return render(request, 'accounts/certificate.html', {
        'user': user,
        'stats': stats,
        'today': today,
        'cert_code': cert_code,
    })


def privacy_policy_view(request):
    """Zásady ochrany osobných údajov (GDPR compliant)."""
    lang = get_active_lang(request)
    return render(request, 'pages/privacy.html', {'ui_lang': lang})


def terms_of_service_view(request):
    """Všeobecné obchodné a licenčné podmienky platformy Codoro."""
    lang = get_active_lang(request)
    return render(request, 'pages/terms.html', {'ui_lang': lang})


def thank_you_view(request):
    """Potvrdzovacia stránka po odoslaní žiadosti alebo registrácii."""
    lang = get_active_lang(request)
    flow_type = request.GET.get('type', 'general')
    return render(request, 'pages/thank_you.html', {'ui_lang': lang, 'flow_type': flow_type})


def robots_txt(request):
    """Dynamický robots.txt pre vyhľadávače."""
    content = """User-agent: *
Allow: /
Allow: /welcome/
Allow: /cheatsheets/
Allow: /get-license/
Allow: /privacy/
Allow: /terms/
Allow: /login/
Allow: /register/
Disallow: /admin/
Disallow: /admin-panel/
Disallow: /teacher/
Disallow: /logout/

Sitemap: https://codoro.sk/sitemap.xml
"""
    return HttpResponse(content.strip(), content_type="text/plain")


def sitemap_xml(request):
    """Štruktúrovaná XML mapa stránok pre SEO."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://codoro.sk/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://codoro.sk/welcome/</loc>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://codoro.sk/cheatsheets/</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://codoro.sk/get-license/</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://codoro.sk/privacy/</loc>
        <changefreq>yearly</changefreq>
        <priority>0.3</priority>
    </url>
    <url>
        <loc>https://codoro.sk/terms/</loc>
        <changefreq>yearly</changefreq>
        <priority>0.3</priority>
    </url>
    <url>
        <loc>https://codoro.sk/login/</loc>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://codoro.sk/register/</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
</urlset>"""
    return HttpResponse(xml_content.strip(), content_type="application/xml")


def custom_400(request, exception=None):
    """Zákaznícka 400 stránka bez surových technických chýb."""
    lang = get_active_lang(request)
    return render(request, '404.html', {
        'ui_lang': lang,
        'error_code': '400',
        'error_title_sk': 'Neplatná požiadavka',
        'error_title_en': 'Bad Request',
        'error_desc_sk': 'Odoslané údaje mali nesprávny formát. Skontroluj prosím formulár a skús to znova.',
        'error_desc_en': 'The submitted data could not be processed. Please check your input and try again.',
    }, status=400)


def custom_403(request, exception=None):
    """Zákaznícka 403 stránka pri zamietnutí prístupu."""
    lang = get_active_lang(request)
    return render(request, '404.html', {
        'ui_lang': lang,
        'error_code': '403',
        'error_title_sk': 'Prístup zamietnutý',
        'error_title_en': 'Access Denied',
        'error_desc_sk': 'Na zobrazenie tejto sekcie nemáš dostatočné oprávnenia.',
        'error_desc_en': 'You do not have permission to access this section.',
    }, status=403)


def custom_404(request, exception=None):
    """Zákaznícka 404 stránka s maskotom Codoro."""
    lang = get_active_lang(request)
    return render(request, '404.html', {
        'ui_lang': lang,
        'error_code': '404',
    }, status=404)


def custom_500(request):
    """Zákaznícka 500 stránka bez odhalenia interného stacktrace."""
    lang = 'sk'
    try:
        lang = get_active_lang(request)
    except Exception:
        pass
    return render(request, '404.html', {
        'ui_lang': lang,
        'error_code': '500',
        'error_title_sk': 'Chyba na strane servera',
        'error_title_en': 'Server Error',
        'error_desc_sk': 'Nastala neočakávaná chyba pri spracovaní požiadavky. Skús obnoviť stránku o chvíľu.',
        'error_desc_en': 'An unexpected error occurred while processing your request. Please try again shortly.',
    }, status=500)


# =========================================================================
# ZABUDNUTÉ HESLO / PASSWORD RESET FLOW (MENO ALEBO EMAIL)
# =========================================================================

def password_reset_request_view(request):
    """
    Formulár na vyžiadanie odkazu na obnovenie hesla.
    Používateľ môže zadať buď prihlasovacie meno, alebo e-mailovú adresu.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    lang = get_active_lang(request)

    if request.method == 'POST':
        if not check_honeypot(request):
            return redirect('password_reset_done')

        if is_rate_limited(request, 'password_reset', limit=8, window_seconds=600):
            err = (
                "Too many password reset requests. Please wait a few minutes."
                if lang == 'en'
                else "Príliš veľa žiadostí o obnovu hesla. Počkaj prosím pár minút."
            )
            messages.error(request, err)
            return render(request, 'accounts/password_reset.html', {'ui_lang': lang}, status=429)

        identity = sanitize_text(request.POST.get('identity', ''), max_length=254)
        if not identity:
            err = "Please enter your username or email." if lang == 'en' else "Zadaj svoje prihlasovacie meno alebo e-mail."
            messages.error(request, err)
            return render(request, 'accounts/password_reset.html', {'ui_lang': lang})

        user = User.objects.filter(
            Q(username__iexact=identity) | Q(email__iexact=identity)
        ).first()

        if user and user.is_active and user.email:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            )

            subject = "Obnovenie hesla — Codoro" if lang == 'sk' else "Password Reset — Codoro"
            text_content = (
                f"Ahoj {user.username},\n\n"
                f"obdržali sme žiadosť o obnovenie hesla pre tvoj účet na platforme Codoro.\n\n"
                f"Pre nastavenie nového hesla klikni na nasledujúci odkaz (platný 24 hodín):\n"
                f"{reset_url}\n\n"
                f"Ak si o zmenu hesla nežiadal(a), túto správu môžeš ignorovať. Tvoje heslo zostane nezmenené.\n\n"
                f"S pozdravom,\nTím Codoro\nhttps://codoro.sk\n"
            ) if lang == 'sk' else (
                f"Hello {user.username},\n\n"
                f"we received a password reset request for your Codoro account.\n\n"
                f"Click the link below to set a new password (valid for 24 hours):\n"
                f"{reset_url}\n\n"
                f"If you did not request this, safely ignore this message. Your password remains unchanged.\n\n"
                f"Best regards,\nCodoro Team\nhttps://codoro.sk\n"
            )

            html_content = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F3F7F5; margin: 0; padding: 24px; color: #111C18;">
  <div style="max-width: 540px; margin: 0 auto; background: #FFFFFF; border-radius: 16px; border: 1px solid #E2ECE7; padding: 32px; box-shadow: 0 8px 24px rgba(14,30,24,0.06);">
    <div style="margin-bottom: 20px;">
      <span style="font-size: 26px; font-weight: 800; color: #008767; letter-spacing: -0.5px;">codo<span style="color: #111C18;">ro</span></span>
    </div>
    <h2 style="font-size: 20px; font-weight: 800; color: #111C18; margin: 0 0 12px;">{'Obnovenie hesla do účtu' if lang == 'sk' else 'Password Reset for Your Account'}</h2>
    <p style="font-size: 14px; line-height: 1.6; color: #4B5E57; margin: 0 0 20px;">
      {'Ahoj' if lang == 'sk' else 'Hello'} <strong>{user.username}</strong>,<br>
      {'obdržali sme žiadosť o vytvorenie nového hesla pre tvoj účet Codoro. Kliknutím na tlačidlo nižšie si nastav nové heslo:' if lang == 'sk' else 'we received a request to create a new password for your Codoro account. Click the button below to set a new password:'}
    </p>
    <div style="text-align: center; margin: 28px 0;">
      <a href="{reset_url}" style="display: inline-block; background: #008767; color: #FFFFFF; font-weight: 700; font-size: 15px; padding: 12px 28px; border-radius: 12px; text-decoration: none; box-shadow: 0 4px 12px rgba(0,135,103,0.25);">
        {'Nastaviť nové heslo →' if lang == 'sk' else 'Set New Password →'}
      </a>
    </div>
    <p style="font-size: 12px; line-height: 1.5; color: #788B83; margin: 20px 0 0; border-top: 1px solid #E2ECE7; padding-top: 16px;">
      {'Tento odkaz je platný 24 hodín. Ak si o zmenu nežiadal(a), môžeš tento e-mail bez obáv ignorovať.' if lang == 'sk' else 'This link is valid for 24 hours. If you did not request a reset, you can safely ignore this email.'}
    </p>
  </div>
</body>
</html>
"""
            try:
                send_mail(
                    subject=subject,
                    message=text_content,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'podpora@codoro.sk'),
                    recipient_list=[user.email],
                    html_message=html_content,
                    fail_silently=True,
                )
            except Exception:
                pass

            # Pre vývoj a ukážku na obhajobe (aby nebolo nutné čakať na reálnu schránku):
            if settings.DEBUG:
                request.session['dev_reset_url'] = reset_url
                request.session['dev_reset_user'] = user.username
                request.session['dev_reset_email'] = user.email

        # Bezpečnostná ochrana (ochrana proti User Enumeration): vždy redirect na done
        return redirect('password_reset_done')

    return render(request, 'accounts/password_reset.html', {'ui_lang': lang})


def password_reset_done_view(request):
    """Informačná stránka o odoslaní odkazu na obnovenie hesla."""
    lang = get_active_lang(request)
    dev_reset_url = request.session.pop('dev_reset_url', None) if settings.DEBUG else None
    dev_reset_user = request.session.pop('dev_reset_user', None) if settings.DEBUG else None
    dev_reset_email = request.session.pop('dev_reset_email', None) if settings.DEBUG else None
    return render(request, 'accounts/password_reset_done.html', {
        'ui_lang': lang,
        'dev_reset_url': dev_reset_url,
        'dev_reset_user': dev_reset_user,
        'dev_reset_email': dev_reset_email,
    })


def password_reset_confirm_view(request, uidb64, token):
    """
    Formulár na zadanie nového hesla po kliknutí na aktivačný odkaz.
    """
    lang = get_active_lang(request)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    validlink = bool(user and default_token_generator.check_token(user, token))

    if not validlink:
        return render(request, 'accounts/password_reset_confirm.html', {
            'ui_lang': lang,
            'validlink': False,
        })

    if request.method == 'POST':
        password = (request.POST.get('password') or request.POST.get('new_password') or '').strip()
        password_confirm = (request.POST.get('password_confirm') or request.POST.get('confirm_password') or '').strip()

        level, is_strong, errs_sk, errs_en = evaluate_password_strength(password)
        if not is_strong:
            err = " ".join(errs_en) if lang == 'en' else " ".join(errs_sk)
            messages.error(request, err)
            return render(request, 'accounts/password_reset_confirm.html', {'ui_lang': lang, 'validlink': True, 'reset_user': user})

        if password != password_confirm:
            err = "Passwords do not match." if lang == 'en' else "Zadané heslá sa nezhodujú."
            messages.error(request, err)
            return render(request, 'accounts/password_reset_confirm.html', {'ui_lang': lang, 'validlink': True, 'reset_user': user})

        if user.is_password_in_history(password):
            err = (
                "New password cannot be the same as your current or any of your last 3 previous passwords."
                if lang == 'en'
                else "Nové heslo sa nesmie zhodovať s aktuálnym ani so žiadnym z tvojich posledných 3 predchádzajúcich hesiel."
            )
            messages.error(request, err)
            return render(request, 'accounts/password_reset_confirm.html', {'ui_lang': lang, 'validlink': True, 'reset_user': user})

        user.record_password_change(password)
        return redirect('password_reset_complete')

    return render(request, 'accounts/password_reset_confirm.html', {
        'ui_lang': lang,
        'validlink': True,
        'reset_user': user,
    })


def password_reset_complete_view(request):
    """Potvrdenie o úspešnej zmene hesla s tlačidlom na prihlásenie."""
    lang = get_active_lang(request)
    return render(request, 'accounts/password_reset_complete.html', {'ui_lang': lang})
