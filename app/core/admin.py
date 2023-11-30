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
    fieldsets=(       #field set is place where we can edit user like edit email or password or it is a place that sets our status which is staff, active, superuser
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
        ),
        (_('Important dates'), {'fields':('last_login',)}),
    )
    readonly_fields = ['last_login'] #to make the field visable for the user but not editable.
    add_fieldsets =(
        (None,{
            'classes':('wide',), #it use for making the pages looks wide
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )
admin.site.register(models.User, UserAdmin) #to make customizable otherwise if we write it without UserAdmin it will be default one.
admin.site.register(models.Recipe)