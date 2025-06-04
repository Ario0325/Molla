from django.shortcuts import render, redirect
from .Forms import ContactUsModuleFrom
from django.urls import reverse
from django.views.generic.edit import CreateView
#from .models import ContactUs

class ContactUsViews(CreateView):
    form_class = ContactUsModuleFrom
    template_name = 'ContactUs_module/Contact.html'
    success_url = '/Contact-us/'