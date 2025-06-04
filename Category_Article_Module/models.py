from django.db import models
from jalali_date import datetime2jalali

class ArticleCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان دسته‌بندی')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='عنوان در url')
    parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE,
                              verbose_name='دسته‌بندی والد')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'دسته‌بندی مقالات'
        verbose_name_plural = 'دسته‌بندی‌های مقالات'
        indexes = [
            models.Index(fields=['url_title']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.title

    def get_jalali_created_date(self):
        return datetime2jalali(self.created_at).strftime('%Y/%m/%d _ %H:%M:%S')

    def get_jalali_updated_date(self):
        return datetime2jalali(self.updated_at).strftime('%Y/%m/%d _ %H:%M:%S')
