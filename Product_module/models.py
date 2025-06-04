from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    image = models.ImageField(upload_to='images/category', verbose_name='تصویر دسته بندی', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال', default=True)
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده', default=False)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class ProductSize(models.Model):
    title = models.CharField(max_length=50, verbose_name='سایز')

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایزها'

    def __str__(self):
        return self.title


class ProductColor(models.Model):
    title = models.CharField(max_length=50, verbose_name='رنگ')
    code = models.CharField(max_length=20, verbose_name='کد رنگ', null=True, blank=True)

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/products', verbose_name='تصویر اصلی')
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')
    price = models.IntegerField(verbose_name='قیمت')
    old_price = models.IntegerField(verbose_name='قیمت قبلی', null=True, blank=True)
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    features = models.TextField(verbose_name='ویژگی ها', null=True, blank=True)
    shipping_info = models.TextField(verbose_name='اطلاعات ارسال', null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    category = models.ManyToManyField(ProductCategory, verbose_name='دسته بندی‌ها', related_name='products')
    sizes = models.ManyToManyField(ProductSize, verbose_name='سایزها', blank=True)
    colors = models.ManyToManyField(ProductColor, verbose_name='رنگ ها', blank=True)
    is_special = models.BooleanField(default=False, verbose_name='محصول ویژه')
    is_new = models.BooleanField(default=False, verbose_name='محصول جدید')
    discount_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                           blank=True, verbose_name='درصد تخفیف')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')

    def save(self, *args, **kwargs):
        if self.stock < 0:
            self.stock = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'
