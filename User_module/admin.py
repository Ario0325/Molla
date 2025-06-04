from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'is_staff', 'mobile', 'profile_image_tag', 'jalali_date_joined')

    def jalali_date_joined(self, obj):
        return obj.get_jalali_date_joined()
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'is_staff', 'mobile', 'profile_image_tag', 'jalali_date_joined')
    jalali_date_joined.short_description = 'تاریخ عضویت'
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'mobile')

    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_image.url)
        return "بدون تصویر"

    profile_image_tag.short_description = 'تصویر پروفایل'

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'mobile', 'profile_image_tag')


admin.site.register(User, CustomUserAdmin)
