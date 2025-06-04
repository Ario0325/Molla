from django.shortcuts import render
from .models import About


def about(request):
    about_me = About.objects.first()

    content = {

        'about_me': about_me
    }

    return render(request, 'AboutUs_module/About.html', content)
