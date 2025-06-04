from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import jalali_converter

class User(AbstractUser):
    mobile = models.CharField(max_length=12, verbose_name='شماره', null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', verbose_name='عکس پروفایل', null=True, blank=True)

    def __str__(self):
        return self.username

    def get_jalali_date_joined(self):
        return jalali_converter(self.date_joined)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
