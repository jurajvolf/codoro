from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SchoolClass, SubscriptionLicense

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'school_class', 'level', 'xp', 'doros', 'current_streak', 'subscription_tier')
    list_filter = ('role', 'subscription_tier', 'school_class', 'preferred_language')
    fieldsets = UserAdmin.fieldsets + (
        ('Codoro Profil & Rola', {'fields': ('role', 'school_class', 'preferred_language', 'subscription_tier')}),
        ('Gamifikácia (XP, Doros, Streak)', {'fields': ('xp', 'level', 'doros', 'current_streak', 'longest_streak', 'streak_freezes')}),
    )

admin.site.register(SchoolClass)
admin.site.register(SubscriptionLicense)