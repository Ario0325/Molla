from django.contrib import admin
from . import models

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'parent', 'is_active', 'get_created_jalali', 'get_updated_jalali']
    list_editable = ['is_active', 'parent']
    list_filter = ['is_active', 'parent']
    search_fields = ['title', 'url_title']
    ordering = ['-created_at']

    @admin.display(description='تاریخ ایجاد')
    def get_created_jalali(self, obj):
        return obj.get_jalali_created_date()

    @admin.display(description='تاریخ بروزرسانی')
    def get_updated_jalali(self, obj):
        return obj.get_jalali_updated_date()

admin.site.register(models.ArticleCategory, ArticleCategoryAdmin)
