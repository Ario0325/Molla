from django.db import models
from jalali_date import datetime2jalali
from Category_Article_Module.models import ArticleCategory
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator

class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=400, unique=True, verbose_name='عنوان در url')
    category = models.ManyToManyField(ArticleCategory, related_name='articles', verbose_name='دسته‌بندی‌ها')
    image = models.ImageField(upload_to='images/articles', verbose_name='تصویر مقاله')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    content = models.TextField(verbose_name='محتوای مقاله')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='نویسنده', null=True)
    view_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    comment_count = models.IntegerField(default=0, verbose_name='تعداد دیدگاه‌ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    reading_time = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='زمان مطالعه (دقیقه)'
    )
    meta_description = models.CharField(max_length=160, verbose_name='متا توضیحات', null=True, blank=True)
    meta_keywords = models.CharField(max_length=200, verbose_name='کلمات کلیدی', null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ انتشار')
    status = models.CharField(max_length=20, choices=[
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده')
    ], default='draft', verbose_name='وضعیت')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status', 'is_active']),
        ]

    def __str__(self):
        return self.title

    def get_jalali_date(self):
        return datetime2jalali(self.created_at).strftime('%Y/%m/%d %H:%M')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article:article-detail', kwargs={'slug': self.slug})
