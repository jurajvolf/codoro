from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
import hashlib
import hmac
import subprocess
import os
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from accounts import views as acc_views
from courses import views as course_views
from gamification import views as game_views
from teacher_panel import views as teacher_views


@csrf_exempt
def git_webhook_update(request):
    """Automaticky stiahne zmeny z GitHubu po každom git push a reštartuje PythonAnywhere."""
    if request.method != 'POST':
        return HttpResponseForbidden("Iba POST požiadavky sú povolené.")

    # Overenie podpisu z GitHubu (vyžaduje nakonfigurovaný GITHUB_WEBHOOK_SECRET v prostredí)
    secret_str = (getattr(settings, 'GITHUB_WEBHOOK_SECRET', '') or '').strip()
    if not secret_str:
        return HttpResponseForbidden("Webhook nie je nakonfigurovaný (chýba GITHUB_WEBHOOK_SECRET).")

    signature = request.headers.get('X-Hub-Signature-256', '')
    secret = secret_str.encode('utf-8')
    expected_sig = 'sha256=' + hmac.new(secret, request.body, hashlib.sha256).hexdigest()

    if not signature or not hmac.compare_digest(signature, expected_sig):
        return HttpResponseForbidden("Neplatný bezpečnostný podpis Webhooku.")

    repo_dir = str(settings.BASE_DIR)
    # 1. Stiahnutie zmien z GitHubu
    subprocess.run(['git', '-C', repo_dir, 'pull'], check=False)

    # 2. Spustenie migrácií a collectstatic priamo cez Django management
    from django.core.management import call_command
    try:
        call_command('migrate', interactive=False)
        call_command('collectstatic', interactive=False)
    except Exception as err:
        # Fallback cez sys.executable ak by priamy beh zlyhal
        pass

    # 3. Automatický reštart WSGI súboru na PythonAnywhere
    wsgi_dir = '/var/www'
    if os.path.exists(wsgi_dir):
        for fname in os.listdir(wsgi_dir):
            if fname.endswith('_wsgi.py'):
                os.utime(os.path.join(wsgi_dir, fname), None)

    return HttpResponse("Codoro server bol úspešne aktualizovaný a reštartovaný!", status=200)


urlpatterns = [
    path('git-update/', git_webhook_update, name='git_webhook_update'),
    path('admin/', admin.site.urls),
    path('admin-panel/', include('admin_panel.urls')),

    # Autentifikácia, obnovenie hesla, jazyk, záchrana Streaku a licencie
    path('login/', acc_views.login_view, name='login'),
    path('register/', acc_views.register_view, name='register'),
    path('logout/', acc_views.logout_view, name='logout'),
    path('password-reset/', acc_views.password_reset_request_view, name='password_reset'),
    path('password-reset/done/', acc_views.password_reset_done_view, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', acc_views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password-reset/complete/', acc_views.password_reset_complete_view, name='password_reset_complete'),
    path('lang/<str:lang_code>/', acc_views.switch_language, name='switch_language'),
    path('streak/repair/', acc_views.repair_streak, name='repair_streak'),
    path('license/activate/', acc_views.activate_license, name='activate_license'),
    path('get-license/', acc_views.get_license_view, name='get_license'),
    path('profile/', acc_views.profile_view, name='profile'),
    path('certificate/', acc_views.certificate_view, name='certificate'),

    # Právne dokumenty, SEO a potvrdenia
    path('privacy/', acc_views.privacy_policy_view, name='privacy_policy'),
    path('terms/', acc_views.terms_of_service_view, name='terms_of_service'),
    path('thank-you/', acc_views.thank_you_view, name='thank_you'),
    path('robots.txt', acc_views.robots_txt, name='robots_txt'),
    path('sitemap.xml', acc_views.sitemap_xml, name='sitemap_xml'),
    path('404/', acc_views.custom_404, name='preview_404'),

    # Študentský Dashboard, Lekcie a Editor kódu
    path('', course_views.dashboard, name='dashboard'),
    path('welcome/', course_views.landing_page, name='landing_page'),
    path('arena/', course_views.practice_arena, name='practice_arena'),
    path('cheatsheets/', course_views.cheat_sheets_view, name='cheat_sheets'),
    path('lesson/<int:lesson_id>/', course_views.lesson_detail, name='lesson_detail'),
    path('exercise/<int:exercise_id>/unlock-hint/', course_views.unlock_hint, name='unlock_hint'),

    # Obchod so zásobami, Questy a Coin Dropy
    path('shop/', game_views.shop_view, name='shop'),
    path('shop/buy/<int:reward_id>/', game_views.buy_reward, name='buy_reward'),
    path('quest/claim/<int:progress_id>/', game_views.claim_quest_reward, name='claim_quest_reward'),
    path('coindrop/claim/<int:drop_id>/', game_views.claim_coin_drop, name='claim_coin_drop'),

    # Vlastný Učiteľský panel (God Mode & CMS štúdio)
    path('teacher/', teacher_views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/student/<int:student_id>/economy/', teacher_views.manage_student_economy, name='manage_student_economy'),
    path('teacher/student/<int:student_id>/', teacher_views.student_detail, name='teacher_student_detail'),
    path('teacher/student/<int:student_id>/assign-class/', teacher_views.cms_student_assign_class, name='cms_student_assign_class'),
    path('teacher/coupon/<int:purchase_id>/', teacher_views.process_coupon, name='process_coupon'),
    path('teacher/class/create/', teacher_views.cms_class_create, name='cms_class_create'),
    path('teacher/class/<int:class_id>/delete/', teacher_views.cms_class_delete, name='cms_class_delete'),
    path('teacher/class/<int:class_id>/batch-students/', teacher_views.cms_class_batch_students, name='cms_class_batch_students'),
    path('teacher/class/<int:class_id>/remove-student/<int:student_id>/', teacher_views.cms_class_remove_student, name='cms_class_remove_student'),
    path('teacher/license/create/', teacher_views.cms_license_create, name='cms_license_create'),

    # CMS - Moduly
    path('teacher/modules/', teacher_views.cms_modules, name='cms_modules'),
    path('teacher/module/create/', teacher_views.cms_module_create, name='cms_module_create'),
    path('teacher/module/<int:module_id>/edit/', teacher_views.cms_module_edit, name='cms_module_edit'),
    path('teacher/module/<int:module_id>/delete/', teacher_views.cms_module_delete, name='cms_module_delete'),
    path('teacher/module/<int:module_id>/reorder/<str:direction>/', teacher_views.cms_module_reorder, name='cms_module_reorder'),
    path('teacher/module/<int:module_id>/toggle-pro/', teacher_views.cms_module_toggle_pro, name='cms_module_toggle_pro'),
    path('teacher/module/<int:module_id>/toggle-publish/', teacher_views.cms_module_toggle_publish, name='cms_module_toggle_publish'),

    # CMS - Lekcie & Kvízy
    path('teacher/module/<int:module_id>/lesson/create/', teacher_views.cms_lesson_create, name='cms_lesson_create'),
    path('teacher/lesson/<int:lesson_id>/edit/', teacher_views.cms_lesson_edit, name='cms_lesson_edit'),
    path('teacher/lesson/<int:lesson_id>/delete/', teacher_views.cms_lesson_delete, name='cms_lesson_delete'),
    path('teacher/lesson/<int:lesson_id>/duplicate/', teacher_views.cms_lesson_duplicate, name='cms_lesson_duplicate'),
    path('teacher/lesson/<int:lesson_id>/quiz/create/', teacher_views.cms_quiz_create, name='cms_quiz_create'),
    path('teacher/quiz/<int:quiz_id>/edit/', teacher_views.cms_quiz_edit, name='cms_quiz_edit'),
    path('teacher/quiz/<int:quiz_id>/delete/', teacher_views.cms_quiz_delete, name='cms_quiz_delete'),

    # CMS - Cvičenia & TestCases & Sandbox Test Runner
    path('teacher/lesson/<int:lesson_id>/exercise/create/', teacher_views.cms_exercise_create, name='cms_exercise_create'),
    path('teacher/exercise/<int:exercise_id>/edit/', teacher_views.cms_exercise_edit, name='cms_exercise_edit'),
    path('teacher/exercise/<int:exercise_id>/delete/', teacher_views.cms_exercise_delete, name='cms_exercise_delete'),
    path('teacher/exercise/<int:exercise_id>/testcase/create/', teacher_views.cms_testcase_create, name='cms_testcase_create'),
    path('teacher/testcase/<int:testcase_id>/edit/', teacher_views.cms_testcase_edit, name='cms_testcase_edit'),
    path('teacher/testcase/<int:testcase_id>/delete/', teacher_views.cms_testcase_delete, name='cms_testcase_delete'),
    path('teacher/test-solution/', teacher_views.cms_test_solution, name='cms_test_solution'),
    path('teacher/exercise/create/', teacher_views.create_exercise, name='create_exercise'),
    path('teacher/submission/<int:submission_id>/comment/', teacher_views.comment_submission, name='comment_submission'),
    path('teacher/exercise/ai-generate/', teacher_views.ai_generate_exercise, name='ai_generate_exercise'),
    path('teacher/exercise/ai-translate/', teacher_views.ai_translate_exercise, name='ai_translate_exercise'),

    # CMS - Obchod, Questy, Dropy
    path('teacher/reward/create/', teacher_views.create_reward_item, name='create_reward_item'),
    path('teacher/reward/<int:reward_id>/edit/', teacher_views.cms_reward_edit, name='cms_reward_edit'),
    path('teacher/reward/<int:reward_id>/restock/', teacher_views.cms_reward_restock, name='cms_reward_restock'),
    path('teacher/reward/<int:reward_id>/toggle-active/', teacher_views.cms_reward_toggle_active, name='cms_reward_toggle_active'),
    path('teacher/reward/<int:reward_id>/delete/', teacher_views.cms_reward_delete, name='cms_reward_delete'),
    path('teacher/coindrop/create/', teacher_views.create_coin_drop, name='create_coin_drop'),
    path('teacher/quest/create/', teacher_views.create_quest, name='create_quest'),
    path('teacher/quest/<int:quest_id>/edit/', teacher_views.cms_quest_edit, name='cms_quest_edit'),
    path('teacher/quest/<int:quest_id>/delete/', teacher_views.cms_quest_delete, name='cms_quest_delete'),
    path('teacher/classquest/create/', teacher_views.create_class_quest, name='create_class_quest'),
    path('teacher/classquest/<int:class_quest_id>/edit/', teacher_views.cms_classquest_edit, name='cms_classquest_edit'),
    path('teacher/classquest/<int:class_quest_id>/delete/', teacher_views.cms_classquest_delete, name='cms_classquest_delete'),
    path('teacher/classquest/<int:class_quest_id>/distribute/', teacher_views.cms_classquest_distribute, name='cms_classquest_distribute'),
    path('404/', acc_views.custom_404, name='preview_404'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': str(settings.STATIC_ROOT if (settings.STATIC_ROOT and settings.STATIC_ROOT.exists()) else (settings.BASE_DIR / 'static'))}),
]

handler400 = 'accounts.views.custom_400'
handler403 = 'accounts.views.custom_403'
handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'
