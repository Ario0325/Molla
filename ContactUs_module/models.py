from django.db import models

# Create your models here.
class ContactUs(models.Model):
    username = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=200, verbose_name='ایمیل')
    phone = models.CharField(max_length=12, verbose_name='شماره تماس')
    text = models.TextField(verbose_name='توضیحات')
    object = models.CharField(verbose_name='موضوع',null=True,max_length=120)