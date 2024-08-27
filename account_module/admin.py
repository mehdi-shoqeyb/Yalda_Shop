from django.contrib import admin
from . import models 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username','profile_picture', 'phone_number','email', 'first_name', 'last_name', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'favorite_products','profile_picture', 'phone_number', 'gender', 'national_code', 'postal_code', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'profile_picture'),
        }),
    )

    
admin.site.register(models.User,CustomUserAdmin)
admin.site.register(models.OTP)