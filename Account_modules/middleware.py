from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class ProfileAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/Account-user/profile/') and not request.user.is_authenticated:
            messages.warning(request, 'برای مشاهده پروفایل، لطفاً وارد حساب کاربری خود شوید.')
            return redirect(reverse('home'))
        return self.get_response(request)
