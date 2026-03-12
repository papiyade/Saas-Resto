from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_platform_admin', 'restaurant', 'is_active')
    list_filter = ('is_platform_admin', 'is_active', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Platform Scope', {'fields': ('is_platform_admin', 'restaurant')}),
    )
