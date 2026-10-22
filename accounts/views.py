from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
import hashlib
import secrets
import re
from .models import User, SchoolClass, SubscriptionLicense, SchoolLicenseRequest
from gamification.models import DorosTransaction, Badge, StudentBadge
from gamification.services import get_student_stats, award_badges, ensure_badges_exist


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
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
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
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        pref_lang = request.POST.get('preferred_language', lang)

        if not username or not password:
            messages.error(request, "Vyplň používateľské meno a heslo." if pref_lang == 'sk' else "Please fill in username and password.")
            return render(request, 'accounts/register.html', {'ui_lang': lang, 'active_tab': account_type})

        if User.objects.filter(username=username).exists():
            err = "This username is already taken." if pref_lang == 'en' else "Toto používateľské meno sa už používa."
            messages.error(request, err)
            return render(request, 'accounts/register.html', {'ui_lang': lang, 'active_tab': account_type})

        # ==========================================================
        # A) REGISTRÁCIA UČITEĽA (TEACHER & SCHOOL ECOSYSTEM)
        # ==========================================================
        if account_type == 'teacher':
            license_code = (request.POST.get('teacher_license_code') or request.POST.get('school_license_key') or '').strip().upper()
            initial_class_name = request.POST.get('initial_class_name', '').strip()

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
        join_code = (request.POST.get('join_code') or request.POST.get('class_code') or '').strip().upper()
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
        school_name = request.POST.get('school_name', '').strip()
        contact_name = (request.POST.get('contact_name') or request.POST.get('contact_person') or '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        estimated_students = int(request.POST.get('estimated_students') or request.POST.get('expected_students') or 30)
        note = request.POST.get('note', '').strip()

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
    
    # 1. Parameter ?next= má najvyššiu prioritu
    next_url = request.GET.get('next')
    if not next_url:
        referer = request.META.get('HTTP_REFERER')
        # Zabránime cykleniu, ak by referer smeroval na prepínač jazyka
        if referer and '/lang/' not in referer:
            next_url = referer

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
        code = request.POST.get('license_code', '').strip().upper()
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
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
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

            if not user.check_password(old_pass):
                err = "Current password is not correct." if lang == 'en' else "Pôvodné heslo nie je správne."
                messages.error(request, err)
            elif len(new_pass) < 6:
                err = "New password must be at least 6 characters long." if lang == 'en' else "Nové heslo musí mať aspoň 6 znakov."
                messages.error(request, err)
            elif new_pass != confirm_pass:
                err = "New passwords do not match." if lang == 'en' else "Nové heslá sa nezhodujú."
                messages.error(request, err)
            else:
                user.set_password(new_pass)
                user.save()
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


def custom_404(request, exception=None):
    """Zákaznícka 404 stránka s maskotom Codoro."""
    lang = get_active_lang(request)
    return render(request, '404.html', {'ui_lang': lang}, status=404)
