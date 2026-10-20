import json
import secrets
import os
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.conf import settings

from accounts.models import User, SchoolClass, SubscriptionLicense
from courses.models import Module, Lesson, Exercise, TestCase, Submission, QuizQuestion, LessonProgress
from gamification.models import (
    RewardItem, RewardPurchase, DorosTransaction, ClassQuest, CoinDrop, Quest, Badge, StudentBadge
)
from courses.curriculum import ALL_CURRICULUM_MODULES


def admin_required(view_func):
    """Dekorátor vyžadujúci prihláseného administrátora (is_superuser, is_staff alebo role ADMIN)."""
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not getattr(request.user, 'is_admin', lambda: False)():
            msg = "Access denied. Administrator privileges required." if getattr(request.user, 'preferred_language', 'sk') == 'en' else "Prístup zamietnutý. Vyžadujú sa administrátorské práva."
            messages.error(request, msg)
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped


# ==============================================================================
# 1. CENTRÁLNY SUPERADMIN DASHBOARD
# ==============================================================================

@admin_required
def admin_dashboard(request):
    """
    Centrálny riadiaci panel pre hlavného administrátora.
    Poskytuje okamžitý Support Helpdesk, správu licencií, databázy, kurikula a logov.
    """
    active_tab = request.GET.get('tab', 'users')
    search_q = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', '')

    # 1. POUŽÍVATELIA PRE SUPPORT DESK
    users_qs = User.objects.select_related('school_class').order_by('-date_joined')
    if search_q:
        users_qs = users_qs.filter(
            Q(username__icontains=search_q) |
            Q(email__icontains=search_q) |
            Q(first_name__icontains=search_q) |
            Q(last_name__icontains=search_q)
        )
    if role_filter:
        users_qs = users_qs.filter(role=role_filter)

    total_users_count = User.objects.count()
    users_list = users_qs[:100]  # Max 100 s rýchlym vyhľadávaním

    # 2. LICENCIE
    licenses = SubscriptionLicense.objects.all().order_by('-created_at')

    # 3. GLOBÁLNE KURIKULUM (18 MODULOV)
    modules = Module.objects.annotate(
        lesson_count=Count('lessons', distinct=True),
        exercise_count=Count('lessons__exercises', distinct=True)
    ).order_by('order')

    # 4. DATABÁZA & SYSTÉMOVÉ METRIKY
    db_path = settings.DATABASES['default']['NAME']
    db_size_mb = 0
    try:
        if os.path.exists(db_path):
            db_size_mb = round(os.path.getsize(db_path) / (1024 * 1024), 2)
    except Exception:
        pass

    db_stats = {
        'total_users': total_users_count,
        'students_count': User.objects.filter(role=User.Role.STUDENT).count(),
        'teachers_count': User.objects.filter(role=User.Role.TEACHER).count(),
        'admins_count': User.objects.filter(role=User.Role.ADMIN).count(),
        'classes_count': SchoolClass.objects.count(),
        'modules_count': Module.objects.count(),
        'lessons_count': Lesson.objects.count(),
        'exercises_count': Exercise.objects.count(),
        'testcases_count': TestCase.objects.count(),
        'submissions_count': Submission.objects.count(),
        'passed_submissions': Submission.objects.filter(status=Submission.Status.PASSED).count(),
        'failed_submissions': Submission.objects.filter(status=Submission.Status.FAILED).count(),
        'total_doros_circulation': User.objects.aggregate(s=Sum('doros'))['s'] or 0,
        'total_xp': User.objects.aggregate(s=Sum('xp'))['s'] or 0,
        'db_size_mb': db_size_mb,
        'db_engine': settings.DATABASES['default']['ENGINE'].split('.')[-1],
        'debug_mode': settings.DEBUG,
    }

    # 5. ŽIVÝ MONITOR ODOVZDANÍ (POSLEDNÝCH 50 SUBMISSIONS)
    submission_filter = request.GET.get('sub_status', '')
    sub_qs = Submission.objects.select_related('student', 'exercise__lesson__module').order_by('-created_at')
    if submission_filter:
        sub_qs = sub_qs.filter(status=submission_filter)
    recent_submissions = sub_qs[:50]

    all_classes = SchoolClass.objects.all().order_by('name')

    return render(request, 'admin_panel/dashboard.html', {
        'active_tab': active_tab,
        'search_q': search_q,
        'role_filter': role_filter,
        'users_list': users_list,
        'total_users_count': total_users_count,
        'licenses': licenses,
        'modules': modules,
        'db_stats': db_stats,
        'recent_submissions': recent_submissions,
        'submission_filter': submission_filter,
        'all_classes': all_classes,
        'roles': User.Role.choices,
        'tiers': User.SubscriptionTier.choices,
    })


# ==============================================================================
# 2. SUPPORT & USER TROUBLESHOOTING (RIEŠENIE PROBLÉMOV POUŽÍVATEĽOV)
# ==============================================================================

@admin_required
def admin_user_set_password(request, user_id):
    """Zmena alebo vygenerovanie nového hesla používateľovi priamo cez web."""
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'generate':
            new_password = f"Codoro{secrets.token_hex(3).capitalize()}!"
        else:
            new_password = request.POST.get('new_password', '').strip()

        if not new_password or len(new_password) < 6:
            messages.error(request, "Heslo musí mať aspoň 6 znakov.")
            return redirect(f"/admin-panel/?tab=users&q={target_user.username}")

        target_user.set_password(new_password)
        target_user.save()
        messages.success(
            request,
            f"Heslo pre používateľa '{target_user.username}' bolo úspešne zmenené na: {new_password}"
        )
    return redirect(f"/admin-panel/?tab=users&q={target_user.username}")


@admin_required
def admin_user_update_role(request, user_id):
    """Zmena roly používateľa (STUDENT / TEACHER / ADMIN)."""
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in User.Role.values:
            target_user.role = new_role
            if new_role == User.Role.ADMIN:
                target_user.is_staff = True
                target_user.is_superuser = True
            elif target_user.id != request.user.id:
                target_user.is_superuser = False
                target_user.is_staff = (new_role == User.Role.TEACHER)
            target_user.save()
            messages.success(request, f"Rola používateľa '{target_user.username}' bola zmenená na {target_user.get_role_display()}.")
    return redirect(f"/admin-panel/?tab=users&q={target_user.username}")


@admin_required
def admin_user_update_tier(request, user_id):
    """Zmena predplatného používateľa (FREE / PRO / EDU)."""
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_tier = request.POST.get('subscription_tier')
        if new_tier in User.SubscriptionTier.values:
            target_user.subscription_tier = new_tier
            target_user.save(update_fields=['subscription_tier'])
            messages.success(request, f"Predplatné pre '{target_user.username}' bolo nastavené na {target_user.get_subscription_tier_display()}.")
    return redirect(f"/admin-panel/?tab=users&q={target_user.username}")


@admin_required
@transaction.atomic
def admin_user_economy(request, user_id):
    """Úprava Doros a XP pre používateľa (s prepočtom levelu)."""
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        doros_change = int(request.POST.get('doros_change', 0))
        xp_change = int(request.POST.get('xp_change', 0))
        reason = request.POST.get('reason', 'Support zásah').strip()

        if doros_change != 0:
            target_user.doros = max(0, target_user.doros + doros_change)
            DorosTransaction.objects.create(
                student=target_user,
                amount=doros_change,
                reason_sk=f"Support ({request.user.username}): {reason}",
                reason_en=f"Support ({request.user.username}): {reason}",
                performed_by_teacher=request.user
            )

        if xp_change != 0:
            target_user.xp = max(0, target_user.xp + xp_change)
            target_user.level = target_user.calculate_level_from_xp()

        target_user.save()
        messages.success(
            request,
            f"Používateľovi '{target_user.username}' bolo upravené: Doros ({doros_change:+d}), XP ({xp_change:+d}). Aktuálny Level: {target_user.level}."
        )
    return redirect(f"/admin-panel/?tab=users&q={target_user.username}")


@admin_required
def admin_user_streak(request, user_id):
    """Support oprava vyhasnutého alebo prerušeného Streaku."""
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        streak_val = max(0, int(request.POST.get('streak_value', 1)))
        target_user.current_streak = streak_val
        target_user.longest_streak = max(target_user.longest_streak, streak_val)
        target_user.lost_streak_value = 0
        target_user.streak_lost_at = None
        target_user.last_activity_date = timezone.localdate()
        target_user.save()
        messages.success(request, f"Streak používateľa '{target_user.username}' bol obnovený na {streak_val} dní.")
    return redirect(f"/admin-panel/?tab=users&q={target_user.username}")


@admin_required
def admin_user_reset_ai(request, user_id):
    """Vynulovanie denného počítadla AI rád (ak FREE používateľovi zamrzol limit)."""
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        target_user.daily_ai_hints_used = 0
        target_user.last_ai_hint_date = timezone.localdate()
        target_user.save(update_fields=['daily_ai_hints_used', 'last_ai_hint_date'])
        messages.success(request, f"Denný limit AI tútora Codo pre '{target_user.username}' bol resetovaný na plný počet.")
    return redirect(f"/admin-panel/?tab=users&q={target_user.username}")


@admin_required
def admin_user_assign_class(request, user_id):
    """Priradenie alebo odhlásenie používateľa zo školskej triedy."""
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        class_id = request.POST.get('school_class_id')
        if class_id:
            sc = get_object_or_404(SchoolClass, id=class_id)
            target_user.school_class = sc
            messages.success(request, f"Používateľ '{target_user.username}' bol zaradený do triedy {sc.name}.")
        else:
            target_user.school_class = None
            messages.info(request, f"Používateľ '{target_user.username}' bol odhlásený z triedy.")
        target_user.save(update_fields=['school_class'])
    return redirect(f"/admin-panel/?tab=users&q={target_user.username}")


@admin_required
def admin_user_toggle_active(request, user_id):
    """Aktivácia alebo zablokovanie účtu (Ban / Unban)."""
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if target_user.id == request.user.id:
            messages.error(request, "Nemôžeš zablokovať svoj vlastný administrátorský účet.")
            return redirect(f"/admin-panel/?tab=users&q={target_user.username}")

        target_user.is_active = not target_user.is_active
        target_user.save(update_fields=['is_active'])
        status_text = "aktivovaný" if target_user.is_active else "zablokovaný (deaktivovaný)"
        messages.success(request, f"Účet '{target_user.username}' bol {status_text}.")
    return redirect(f"/admin-panel/?tab=users&q={target_user.username}")


@admin_required
def admin_user_delete(request, user_id):
    """Úplné odstránenie účtu z databázy."""
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if target_user.id == request.user.id:
            messages.error(request, "Nemôžeš zmazať svoj vlastný administrátorský účet.")
            return redirect("/admin-panel/?tab=users")

        username = target_user.username
        target_user.delete()
        messages.success(request, f"Používateľský účet '{username}' bol trvalo vymazaný z databázy.")
    return redirect("/admin-panel/?tab=users")


# ==============================================================================
# 3. SPRÁVA LICENCIÍ (LICENSE MANAGEMENT)
# ==============================================================================

@admin_required
def admin_license_create(request):
    """Vytvorenie nového licenčného kľúča (EDU / PRO)."""
    if request.method == 'POST':
        tier = request.POST.get('tier', User.SubscriptionTier.EDU)
        max_uses = int(request.POST.get('max_uses', 30))
        code = request.POST.get('code', '').strip().upper()

        if not code:
            suffix = secrets.token_hex(3).upper()
            code = f"{tier}-{timezone.now().year}-{suffix}"

        if SubscriptionLicense.objects.filter(code=code).exists():
            messages.error(request, f"Licenčný kód '{code}' už v databáze existuje.")
            return redirect('/admin-panel/?tab=licenses')

        lic = SubscriptionLicense.objects.create(code=code, tier=tier, max_uses=max_uses, is_active=True)
        messages.success(request, f"Licenčný kľúč '{lic.code}' ({tier}, max {max_uses} použití) bol úspešne vygenerovaný.")
    return redirect('/admin-panel/?tab=licenses')


@admin_required
def admin_license_toggle(request, license_id):
    """Zapnutie / vypnutie platnosti licencie."""
    lic = get_object_or_404(SubscriptionLicense, id=license_id)
    if request.method == 'POST':
        lic.is_active = not lic.is_active
        lic.save(update_fields=['is_active'])
        status_text = "aktivovaná" if lic.is_active else "deaktivovaná"
        messages.success(request, f"Licencia '{lic.code}' bola {status_text}.")
    return redirect('/admin-panel/?tab=licenses')


@admin_required
def admin_license_delete(request, license_id):
    """Zmazanie licenčného kľúča."""
    lic = get_object_or_404(SubscriptionLicense, id=license_id)
    if request.method == 'POST':
        code = lic.code
        lic.delete()
        messages.success(request, f"Licenčný kľúč '{code}' bol vymazaný.")
    return redirect('/admin-panel/?tab=licenses')


@admin_required
@transaction.atomic
def admin_license_quick_assign(request):
    """Rýchla aktivácia licencie pre konkrétneho používateľa zadaním mena."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        license_id = request.POST.get('license_id')

        target_user = User.objects.filter(username=username).first()
        lic = get_object_or_404(SubscriptionLicense.objects.select_for_update(), id=license_id)

        if not target_user:
            messages.error(request, f"Používateľ s menom '{username}' neexistuje.")
            return redirect('/admin-panel/?tab=licenses')

        if not lic.is_active or lic.current_uses >= lic.max_uses:
            messages.error(request, f"Licencia '{lic.code}' je neaktívna alebo vyčerpaná.")
            return redirect('/admin-panel/?tab=licenses')

        target_user.subscription_tier = lic.tier
        target_user.save(update_fields=['subscription_tier'])
        lic.current_uses += 1
        lic.save(update_fields=['current_uses'])

        messages.success(
            request,
            f"Licencia '{lic.code}' ({lic.tier}) bola úspešne priradená používateľovi '{target_user.username}'."
        )
    return redirect('/admin-panel/?tab=licenses')


# ==============================================================================
# 4. GLOBÁLNE KURIKULUM (CONTENT ACTIONS)
# ==============================================================================

@admin_required
def admin_module_toggle_pro(request, module_id):
    """Rýchle prepnutie FREE <-> PRO/EDU pre modul kurikula."""
    mod = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        mod.is_pro_only = not mod.is_pro_only
        mod.save(update_fields=['is_pro_only'])
        status_text = "PRO / EDU" if mod.is_pro_only else "FREE"
        messages.success(request, f"Modul {mod.order:02d} ({mod.title_sk}) je teraz {status_text}.")
    return redirect('/admin-panel/?tab=curriculum')


@admin_required
def admin_module_toggle_publish(request, module_id):
    """Publikovanie alebo stiahnutie modulu do konceptu."""
    mod = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        mod.is_published = not mod.is_published
        mod.save(update_fields=['is_published'])
        status_text = "publikovaný" if mod.is_published else "skrytý (koncept)"
        messages.success(request, f"Modul {mod.order:02d} ({mod.title_sk}) je teraz {status_text}.")
    return redirect('/admin-panel/?tab=curriculum')


@admin_required
def admin_sync_curriculum(request):
    """
    Bezpečná synchronizácia / aktualizácia kurikula zo šablón mod01 až mod18.
    Aktualizuje znenia úloh, test cases a teórie bez zmazania odovzdaných riešení a profilov!
    """
    if request.method == 'POST':
        synced_modules = 0
        synced_lessons = 0
        synced_exercises = 0

        for mod_data in ALL_CURRICULUM_MODULES:
            mod, _ = Module.objects.update_or_create(
                order=mod_data['order'],
                defaults={
                    'title_sk': mod_data['title_sk'],
                    'title_en': mod_data['title_en'],
                    'description_sk': mod_data['description_sk'],
                    'description_en': mod_data['description_en'],
                    'track': mod_data.get('track', 'FUNDAMENTALS'),
                    'difficulty_level': mod_data.get('difficulty_level', 'BEGINNER'),
                    'estimated_hours': mod_data.get('estimated_hours', 10),
                    'is_pro_only': mod_data.get('is_pro_only', False),
                    'is_published': True,
                }
            )
            synced_modules += 1

            for les_data in mod_data.get('lessons', []):
                les, _ = Lesson.objects.update_or_create(
                    module=mod,
                    order=les_data['order'],
                    defaults={
                        'title_sk': les_data['title_sk'],
                        'title_en': les_data['title_en'],
                        'summary_sk': les_data.get('summary_sk', ''),
                        'summary_en': les_data.get('summary_en', ''),
                        'content_sk': les_data.get('content_sk', ''),
                        'content_en': les_data.get('content_en', ''),
                        'estimated_minutes': les_data.get('estimated_minutes', 45),
                        'xp_reward': les_data.get('xp_reward', 25),
                        'is_published': True,
                    }
                )
                synced_lessons += 1

                for ex_data in les_data.get('exercises', []):
                    ex, _ = Exercise.objects.update_or_create(
                        lesson=les,
                        order=ex_data['order'],
                        defaults={
                            'title_sk': ex_data['title_sk'],
                            'title_en': ex_data['title_en'],
                            'description_sk': ex_data['description_sk'],
                            'description_en': ex_data['description_en'],
                            'starter_code': ex_data['starter_code'],
                            'solution_code': ex_data.get('solution_code', ''),
                            'hint_sk': ex_data.get('hint_sk', ''),
                            'hint_en': ex_data.get('hint_en', ''),
                            'hint_cost_doros': ex_data.get('hint_cost_doros', 15),
                            'xp_reward': ex_data.get('xp_reward', 30),
                            'doros_reward': ex_data.get('doros_reward', 25),
                            'difficulty': ex_data.get('difficulty', 'EASY'),
                        }
                    )
                    synced_exercises += 1

                    for tc_data in ex_data.get('test_cases', []):
                        TestCase.objects.update_or_create(
                            exercise=ex,
                            assert_code=tc_data['assert_code'],
                            defaults={
                                'expected_output': tc_data.get('expected_output', ''),
                                'is_hidden': tc_data.get('is_hidden', False),
                            }
                        )

        messages.success(
            request,
            f"Kurikulum úspešne zosynchronizované! ({synced_modules} modulov, {synced_lessons} lekcií, {synced_exercises} cvičení aktualizovaných)."
        )
    return redirect('/admin-panel/?tab=curriculum')


# ==============================================================================
# 5. DATABÁZA & SYSTÉMOVÁ ÚDRŽBA (MAINTENANCE)
# ==============================================================================

@admin_required
def admin_recalc_levels(request):
    """Prepočíta level zo získaných XP pre všetkých používateľov."""
    if request.method == 'POST':
        updated = 0
        for u in User.objects.all():
            correct_lvl = u.calculate_level_from_xp()
            if u.level != correct_lvl:
                u.level = correct_lvl
                u.save(update_fields=['level'])
                updated += 1
        messages.success(request, f"Kontrola levelov dokončená. Opravených {updated} používateľov.")
    return redirect('/admin-panel/?tab=database')


@admin_required
def admin_refresh_all_streaks(request):
    """Spustí kontrolu a prepočet Streaku pre všetkých používateľov."""
    if request.method == 'POST':
        affected = 0
        for u in User.objects.all():
            if u.refresh_streak_state():
                affected += 1
        messages.success(request, f"Kontrola denných sérií (Streak) dokončená. Aktualizovaných {affected} používateľov.")
    return redirect('/admin-panel/?tab=database')


@admin_required
def admin_clean_submissions(request):
    """Prečistí staré neúspešné testovacie submissions staršie ako 30 dní."""
    if request.method == 'POST':
        cutoff = timezone.now() - timedelta(days=30)
        deleted, _ = Submission.objects.filter(
            status=Submission.Status.FAILED,
            created_at__lt=cutoff
        ).delete()
        messages.success(request, f"Údržba dokončená. Vymazaných {deleted} starých neúspešných submissions.")
    return redirect('/admin-panel/?tab=database')


@admin_required
def admin_export_backup_json(request):
    """Vyexportuje základné dáta platformy Codoro do stiahnuteľného JSON súboru."""
    data = {
        'exported_at': timezone.now().isoformat(),
        'users': [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'role': u.role,
                'tier': u.subscription_tier,
                'xp': u.xp,
                'level': u.level,
                'doros': u.doros,
                'streak': u.current_streak,
                'school_class': u.school_class.name if u.school_class else None,
            }
            for u in User.objects.select_related('school_class').all()
        ],
        'school_classes': [
            {
                'id': sc.id,
                'name': sc.name,
                'join_code': sc.join_code,
                'teacher': sc.teacher.username,
            }
            for sc in SchoolClass.objects.select_related('teacher').all()
        ],
        'licenses': [
            {
                'code': lic.code,
                'tier': lic.tier,
                'max_uses': lic.max_uses,
                'current_uses': lic.current_uses,
                'is_active': lic.is_active,
            }
            for lic in SubscriptionLicense.objects.all()
        ],
        'modules_summary': [
            {
                'order': m.order,
                'title_sk': m.title_sk,
                'track': m.track,
                'is_pro_only': m.is_pro_only,
                'lesson_count': m.lessons.count(),
            }
            for m in Module.objects.all()
        ]
    }

    response = HttpResponse(
        json.dumps(data, indent=2, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )
    filename = f"codoro_backup_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
