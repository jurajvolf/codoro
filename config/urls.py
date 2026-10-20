from django.contrib import admin
from django.urls import path, include
from accounts import views as acc_views
from courses import views as course_views
from gamification import views as game_views
from teacher_panel import views as teacher_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('admin_panel.urls')),

    # Autentifikácia, jazyk, záchrana Streaku a licencie
    path('login/', acc_views.login_view, name='login'),
    path('register/', acc_views.register_view, name='register'),
    path('logout/', acc_views.logout_view, name='logout'),
    path('lang/<str:lang_code>/', acc_views.switch_language, name='switch_language'),
    path('streak/repair/', acc_views.repair_streak, name='repair_streak'),
    path('license/activate/', acc_views.activate_license, name='activate_license'),
    path('profile/', acc_views.profile_view, name='profile'),
    path('certificate/', acc_views.certificate_view, name='certificate'),

    # Študentský Dashboard, Lekcie a Editor kódu
    path('', course_views.dashboard, name='dashboard'),
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
]