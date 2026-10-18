from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import User, SchoolClass, SubscriptionLicense
from gamification.models import DorosTransaction


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
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        join_code = request.POST.get('join_code', '').strip().upper()
        pref_lang = request.POST.get('preferred_language', lang)

        if User.objects.filter(username=username).exists():
            err = "This username is already taken." if pref_lang == 'en' else "Toto používateľské meno sa už používa."
            messages.error(request, err)
            return render(request, 'accounts/register.html', {'ui_lang': lang})

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

    return render(request, 'accounts/register.html', {'ui_lang': lang})


@login_required
def logout_view(request):
    lang = request.user.preferred_language
    logout(request)
    request.session['ui_lang'] = lang
    return redirect('login')


def switch_language(request, lang_code):
    """Prepne jazyk rozhrania pre prihláseného aj neprihláseného používateľa."""
    if lang_code in ['sk', 'en']:
        request.session['ui_lang'] = lang_code
        if request.user.is_authenticated:
            request.user.preferred_language = lang_code
            request.user.save(update_fields=['preferred_language'])
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


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