from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from Product_module.models import Product


class Cart(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'در انتظار پرداخت'),
        ('SUCCESS', 'موفق'),
        ('FAILED', 'ناموفق'),
        ('CANCELED', 'لغو شده'),
        ('ERROR', 'خطا'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پرداخت')
    payment_ref_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='کد پیگیری')
    payment_authority = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING',
                                  verbose_name='وضعیت پرداخت')

    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره تماس')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    postal_code = models.CharField(max_length=10, null=True, blank=True, verbose_name='کد پستی')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_items_count(self):
        return sum(item.quantity for item in self.items.all())

    def update_stock(self):
        for item in self.items.all():
            product = item.product
            if product.stock < item.quantity:
                raise ValidationError(f'موجودی محصول {product.title} کافی نیست')
            product.stock -= item.quantity
            product.save()

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    size = models.CharField(max_length=20, null=True, blank=True, verbose_name='سایز')
    color = models.CharField(max_length=20, null=True, blank=True, verbose_name='رنگ')

    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم های سبد خرید'

    def get_total_price(self):
        return self.quantity * self.product.price
