from django.contrib import admin
from .models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'email', 'text']


# Register your models here.
admin.site.register(ContactUs, ContactUsAdmin)