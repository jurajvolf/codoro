from django.urls import path
from . import views

urlpatterns = [
    # Hlavný SuperAdmin Hub
    path('', views.admin_dashboard, name='admin_dashboard'),

    # Support & User Helpdesk
    path('user/<int:user_id>/password/', views.admin_user_set_password, name='admin_user_set_password'),
    path('user/<int:user_id>/role/', views.admin_user_update_role, name='admin_user_update_role'),
    path('user/<int:user_id>/tier/', views.admin_user_update_tier, name='admin_user_update_tier'),
    path('user/<int:user_id>/economy/', views.admin_user_economy, name='admin_user_economy'),
    path('user/<int:user_id>/streak/', views.admin_user_streak, name='admin_user_streak'),
    path('user/<int:user_id>/reset-ai/', views.admin_user_reset_ai, name='admin_user_reset_ai'),
    path('user/<int:user_id>/assign-class/', views.admin_user_assign_class, name='admin_user_assign_class'),
    path('user/<int:user_id>/toggle-active/', views.admin_user_toggle_active, name='admin_user_toggle_active'),
    path('user/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),

    # Licencie a žiadosti škôl
    path('license/create/', views.admin_license_create, name='admin_license_create'),
    path('license/<int:license_id>/toggle/', views.admin_license_toggle, name='admin_license_toggle'),
    path('license/<int:license_id>/delete/', views.admin_license_delete, name='admin_license_delete'),
    path('license/quick-assign/', views.admin_license_quick_assign, name='admin_license_quick_assign'),
    path('license/request/<int:request_id>/approve/', views.admin_license_request_approve, name='admin_license_request_approve'),
    path('license/request/<int:request_id>/reject/', views.admin_license_request_reject, name='admin_license_request_reject'),

    # Globálne kurikulum
    path('module/<int:module_id>/toggle-pro/', views.admin_module_toggle_pro, name='admin_module_toggle_pro'),
    path('module/<int:module_id>/toggle-publish/', views.admin_module_toggle_publish, name='admin_module_toggle_publish'),
    path('curriculum/sync/', views.admin_sync_curriculum, name='admin_sync_curriculum'),

    # Databáza a systémová údržba
    path('database/recalc-levels/', views.admin_recalc_levels, name='admin_recalc_levels'),
    path('database/refresh-streaks/', views.admin_refresh_all_streaks, name='admin_refresh_all_streaks'),
    path('database/clean-submissions/', views.admin_clean_submissions, name='admin_clean_submissions'),
    path('database/export-json/', views.admin_export_backup_json, name='admin_export_backup_json'),
]
