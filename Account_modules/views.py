# from django.contrib.auth import login, logout
# from django.shortcuts import render, redirect, reverse
# from django.views.generic.base import View
# from User_module.models import User
# from .forms import LoginForm, RegisterForms
# from django.views import View
# from django.shortcuts import render, redirect
# from django.urls import reverse
# from django.contrib.auth import login
# from django.contrib.auth.models import User
# from .forms import RegisterForms
# class RegisterView(View):
#     def get(self, request):
#
#         register_form = RegisterForms()
#         content = {
#             'register_form': register_form
#         }
#         return render(request, 'Account_modules/Login_Register.html', content)
#
#     def post(self, request):
#         register_form = RegisterForms(request.POST)
#         if register_form.is_valid():
#             email = register_form.cleaned_data.get('Email')
#             password = register_form.cleaned_data.get('Password')
#             user: bool = User.objects.filter(email__iexact=email).exists()
#             if user:
#                 register_form.add_error("Email", 'ایمیل وارد شده تکراری میباشد')
#             else:
#                 new_user = User(email=email, is_active=False, username=email)
#                 new_user.set_password(password)
#                 new_user.save()
#                 login(request, new_user)
#                 return redirect(reverse('home'))
#         register_form = RegisterForms()
#         content = {
#             'register_form': register_form
#         }
#         return render(request, 'Account_modules/Login_Register.html', content)
#
#
#
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from .forms import LoginForm, RegisterForms
from User_module.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ProfileEditForm
from User_module.models import User
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from .forms import PasswordResetForm, SetNewPasswordForm
from User_module.models import User
class Login(View):
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('Email')
            password = login_form.cleaned_data.get('Password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید')
                return redirect(reverse('home'))
            else:
                messages.error(request, 'ایمیل یا رمز عبور اشتباه است')
        else:
            messages.error(request, 'اطلاعات وارد شده نامعتبر است')
        return redirect(request.META.get('HTTP_REFERER', reverse('home')))


class RegisterView(View):
    def post(self, request):
        register_form = RegisterForms(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data.get('Email')
            password = register_form.cleaned_data.get('Password')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': email, 'is_active': True}
            )

            if not created:
                messages.error(request, 'ایمیل وارد شده تکراری می‌باشد')
            else:
                user.set_password(password)
                user.save()
                login(request, user)
                messages.success(request, 'ثبت نام شما با موفقیت انجام شد')
                return redirect(reverse('home'))
        else:
            for field, errors in register_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return redirect(request.META.get('HTTP_REFERER', reverse('home')))


def logout_view(request):
    logout(request)
    messages.info(request, 'شما با موفقیت از حساب کاربری خود خارج شدید')
    return redirect('home')
class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'Account_modules/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        if User.objects.filter(username=user.username).exclude(pk=user.pk).exists():
            form.add_error('username', 'این نام کاربری قبلاً استفاده شده است.')
            return self.form_invalid(form)
        messages.success(self.request, 'پروفایل شما با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class PasswordResetView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'Account_modules/password_reset.html', {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']

            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                logout(request)
                messages.success(request, 'رمز عبور با موفقیت تغییر کرد. لطفا با رمز عبور جدید وارد شوید')
                return redirect('home')
            except User.DoesNotExist:
                messages.error(request, 'کاربری با این ایمیل یافت نشد')

        return render(request, 'Account_modules/password_reset.html', {'form': form})


class PasswordResetConfirmView(View):
    template_name = 'Account_modules/password_reset_confirm.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetNewPasswordForm()
            return render(request, self.template_name, {
                'form': form,
                'uidb64': uidb64,
                'token': token
            })

        messages.error(request, 'لینک بازیابی نامعتبر است')
        return redirect('home')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')
                return redirect('Login-Register')
            return render(request, self.template_name, {
                'form': form,
                'uidb64': uidb64,
                'token': token
            })

        messages.error(request, 'لینک بازیابی نامعتبر است')
        return redirect('home')