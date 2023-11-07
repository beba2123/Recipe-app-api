"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models

# Register your models here.

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ('email', 'name')


admin.site.register(models.User, UserAdmin) #to make customizable otherwise if we write it without UserAdmin it will be default one.
