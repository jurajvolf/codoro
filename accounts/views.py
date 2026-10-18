from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import User, SchoolClass, SubscriptionLicense
from gamification.models import DorosTransaction


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Nesprávne prihlasovacie meno alebo heslo.")

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        join_code = request.POST.get('join_code', '').strip().upper()
        lang = request.POST.get('preferred_language', 'sk')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Používateľské meno sa už používa.")
            return render(request, 'accounts/register.html')

        school_class = None
        if join_code:
            school_class = SchoolClass.objects.filter(join_code=join_code).first()
            if not school_class:
                messages.warning(request, "Zadaný kód triedy neexistuje. Účet bol vytvorený bez priradenej triedy.")

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=User.Role.STUDENT,
            school_class=school_class,
            preferred_language=lang,
            doros=100
        )
        DorosTransaction.objects.create(
            student=user,
            amount=100,
            reason_sk="Uvítací bonus za registráciu do Codoro",
            reason_en="Welcome bonus for registering on Codoro"
        )
        login(request, user)
        messages.success(request, "Vitaj v Codoro! Získal si štartovacích 100 Doros.")
        return redirect('dashboard')

    return render(request, 'accounts/register.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def switch_language(request, lang_code):
    if lang_code in ['sk', 'en']:
        request.user.preferred_language = lang_code
        request.user.save(update_fields=['preferred_language'])
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
@transaction.atomic
def repair_streak(request):
    """Umožní študentovi opraviť vyhasnutý Streak za 200 Doros."""
    user = request.user
    repair_cost = 200

    if user.lost_streak_value <= 0:
        messages.info(request, "Nemáš žiadny vyhasnutý Streak na opravu.")
        return redirect('dashboard')

    if user.doros < repair_cost:
        messages.error(request, f"Na opravu Streaku potrebuješ {repair_cost} Doros.")
        return redirect('dashboard')

    user.doros -= repair_cost
    user.current_streak = user.lost_streak_value
    user.lost_streak_value = 0
    user.streak_lost_at = None
    user.save()

    DorosTransaction.objects.create(
        student=user,
        amount=-repair_cost,
        reason_sk=f"Záchrana {user.current_streak}-dňového Streaku",
        reason_en=f"Repaired {user.current_streak}-day Streak"
    )
    messages.success(request, f"🔥 Tvoj {user.current_streak}-dňový Streak bol úspešne obnovený!")
    return redirect('dashboard')


@login_required
@transaction.atomic
def activate_license(request):
    """Aktivácia školského licenčného kľúča (napr. EDU-2027-IVC) alebo simulovaný prechod na PRO."""
    if request.method == 'POST':
        code = request.POST.get('license_code', '').strip().upper()
        lic = SubscriptionLicense.objects.select_for_update().filter(code=code, is_active=True).first()

        if not lic or lic.current_uses >= lic.max_uses:
            messages.error(request, "Neplatný alebo vyčerpaný licenčný kľúč.")
            return redirect('shop')

        request.user.subscription_tier = lic.tier
        request.user.save(update_fields=['subscription_tier'])
        lic.current_uses += 1
        lic.save(update_fields=['current_uses'])

        messages.success(request, f"🎉 Licencia {code} bola aktivovaná! Máš plný prístup k PRO/EDU obsahu a neobmedzenému AI tútorovi Codo.")
    return redirect('shop')