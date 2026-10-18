from django.contrib import admin
from django.urls import path
from accounts import views as acc_views
from courses import views as course_views
from gamification import views as game_views
from teacher_panel import views as teacher_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autentifikácia, jazyk, záchrana Streaku a licencie
    path('login/', acc_views.login_view, name='login'),
    path('register/', acc_views.register_view, name='register'),
    path('logout/', acc_views.logout_view, name='logout'),
    path('lang/<str:lang_code>/', acc_views.switch_language, name='switch_language'),
    path('streak/repair/', acc_views.repair_streak, name='repair_streak'),
    path('license/activate/', acc_views.activate_license, name='activate_license'),

    # Študentský Dashboard, Lekcie a Editor kódu
    path('', course_views.dashboard, name='dashboard'),
    path('lesson/<int:lesson_id>/', course_views.lesson_detail, name='lesson_detail'),
    path('exercise/<int:exercise_id>/unlock-hint/', course_views.unlock_hint, name='unlock_hint'),

    # Obchod so zásobami, Questy a Coin Dropy
    path('shop/', game_views.shop_view, name='shop'),
    path('shop/buy/<int:reward_id>/', game_views.buy_reward, name='buy_reward'),
    path('quest/claim/<int:progress_id>/', game_views.claim_quest_reward, name='claim_quest_reward'),
    path('coindrop/claim/<int:drop_id>/', game_views.claim_coin_drop, name='claim_coin_drop'),

    # Vlastný Učiteľský panel (God Mode & CMS)
    path('teacher/', teacher_views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/student/<int:student_id>/economy/', teacher_views.manage_student_economy, name='manage_student_economy'),
    path('teacher/coupon/<int:purchase_id>/', teacher_views.process_coupon, name='process_coupon'),
    path('teacher/reward/create/', teacher_views.create_reward_item, name='create_reward_item'),
    path('teacher/coindrop/create/', teacher_views.create_coin_drop, name='create_coin_drop'),
    path('teacher/exercise/create/', teacher_views.create_exercise, name='create_exercise'),
]