from django.contrib import admin
from django.utils.html import format_html
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at', 'view_count', 'is_active']
    list_filter = ['status', 'is_active', 'created_at', 'category']
    search_fields = ['title', 'content', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    list_editable = ['status', 'is_active']
    filter_horizontal = ('category',)

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': (
                ('title', 'slug'),
                'author',
                'image',
                'short_description',
                'content'
            ),
            'classes': ('wide',)
        }),
        ('تنظیمات انتشار', {
            'fields': (
                ('status', 'is_active'),
                'published_at',
                'category'
            ),
            'classes': ('collapse',)
        }),
        ('متا', {
            'fields': (
                'meta_description',
                'meta_keywords',
                'reading_time'
            ),
            'classes': ('collapse',)
        })
    )

    class Media:
        css = {
            'all': ('assets/css/custom_admin.css',)
        }
        js = ('assets/js/custom_admin.js',)
