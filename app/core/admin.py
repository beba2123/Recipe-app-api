"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _  # import translation for diffrent languages in Django

# Register your models here.

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ('email', 'name')
    fieldsets=(
        (None, {'fields': ('email', 'password')}),
        (
            _('permission'),
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        )
    )

admin.site.register(models.User, UserAdmin) #to make customizable otherwise if we write it without UserAdmin it will be default one.
