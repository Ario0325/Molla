# from django import forms
# from django.core.validators import MaxLengthValidator, EmailValidator,MinLengthValidator, RegexValidator
# from validators import ValidationError
#
#
# class LoginForm(forms.Form):
#     Email = forms.EmailField(
#         label='ایمیل',
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Email',
#             # 'class': 'form-control',
#             # 'id': 'singin-email',
#             'name': 'email'
#         }),
#         max_length=150,
#         validators=[
#             MaxLengthValidator(150),
#             EmailValidator()
#         ],
#         error_messages={
#             'required': 'وارد کردن ایمیل الزامی می‌باشد',
#             'max_length': 'طول ایمیل نباید بیشتر از 150 کاراکتر باشد'
#         }
#     )
#     Password = forms.CharField(
#         label='رمز عبور',
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Password',
#             # 'id': 'singin-password',
#             'name': 'pswd',
#         }),
#         validators=[
#             MaxLengthValidator(300),
#         ],
#     )
#
#
# class RegisterForms(forms.Form):
#     Email = forms.EmailField(
#         label='ایمیل',
#         widget=forms.TextInput(attrs={
#             'placeholder': 'ایمیل',
#             # 'class': 'form-control',
#             # 'id': 'register-email',
#             'name': 'email'
#         }),
#         max_length=150,
#         validators=[
#             MaxLengthValidator(150),
#             EmailValidator()
#         ],
#
#     )
#     Password = forms.CharField(
#         label='رمز عبور',
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Password',
#             # 'id': 'register-password',
#             'name': 'pswd',
#         }),
#         validators=[
#             MinLengthValidator(8, message='رمز عبور باید حداقل 8 کاراکتر باشد.'),
#             RegexValidator(
#                 regex=r'^\d+$',
#                 message='رمز عبور باید تنها شامل اعداد باشد.'
#             ),
#         ],
#     )
#
#     Confirm_Password = forms.CharField(
#         label='تکرار رمز عبور',
#         widget=forms.PasswordInput(),
#         validators=[
#             MinLengthValidator(8, message='رمز عبور باید حداقل 8 کاراکتر باشد.'),
#             RegexValidator(
#                 regex=r'^\d+$',
#                 message='رمز عبور باید تنها شامل اعداد باشد.'
#             ),
#         ],
#     )
#
#
#     def clean_Confrim_password(self):
#         password = self.cleaned_data.get('Password')
#         confrim_password = self.cleaned_data.get('Confrim_Password')
#         if password == confrim_password:
#             return confrim_password
#         raise ValidationError('رمز و عبور و تکرار رمز عبور صحیح نمیباشد')
#
#
from django import forms
from django.core.validators import MaxLengthValidator, EmailValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from User_module.models import User


class LoginForm(forms.Form):
    Email = forms.EmailField(
        label='ایمیل',
        widget=forms.TextInput(attrs={
            'placeholder': 'Email',
            'name': 'email'
        }),
        max_length=150,
        validators=[
            MaxLengthValidator(150),
            EmailValidator()
        ],
        error_messages={
            'required': 'وارد کردن ایمیل الزامی می‌باشد',
            'max_length': 'طول ایمیل نباید بیشتر از 150 کاراکتر باشد',
            'invalid': 'لطفا یک آدرس ایمیل معتبر وارد کنید'
        }
    )
    Password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'name': 'pswd',
        }),
        validators=[
            MinLengthValidator(8, message='رمز عبور باید حداقل 8 کاراکتر باشد.'),
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message='رمز عبور باید شامل حروف و اعداد باشد.'
            ),
        ],
        error_messages={
            'required': 'وارد کردن رمز عبور الزامی است'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('Email')
        password = cleaned_data.get('Password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise ValidationError('ایمیل یا رمز عبور اشتباه است')
        return cleaned_data


class RegisterForms(forms.Form):
    Email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={
            'placeholder': 'Email',
            'name': 'email'
        }),
        max_length=150,
        validators=[
            MaxLengthValidator(150),
            EmailValidator()
        ],
        error_messages={
            'required': 'وارد کردن ایمیل الزامی می‌باشد',
            'max_length': 'طول ایمیل نباید بیشتر از 150 کاراکتر باشد',
            'invalid': 'لطفا یک آدرس ایمیل معتبر وارد کنید'
        }
    )
    Password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'name': 'pswd',
        }),
        validators=[
            MinLengthValidator(8, message='رمز عبور باید حداقل 8 کاراکتر باشد.'),
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message='رمز عبور باید شامل حروف و سپس اعداد باشد.'
            ),
        ],
        error_messages={
            'required': 'وارد کردن رمز عبور الزامی است'
        }
    )
    Confirm_Password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
        }),
        validators=[
            MinLengthValidator(8, message='رمز عبور باید حداقل 8 کاراکتر باشد.'),
        ],
        error_messages={
            'required': 'تکرار رمز عبور الزامی است'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('Password')
        confirm_password = cleaned_data.get('Confirm_Password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('رمز عبور و تکرار رمز عبور مطابقت ندارند')
        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'لطفاً یک نام کاربری جدید وارد کنید.'


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید'
        })
    )
    new_password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید'
        }),
        validators=[
            MinLengthValidator(8, message='رمز عبور باید حداقل 8 کاراکتر باشد.'),
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message='رمز عبور باید شامل حروف و اعداد باشد.'
            ),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور جدید'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError('رمز عبور و تکرار آن مطابقت ندارند')
        return cleaned_data


class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '*********',
            'id': 'register-password-3'
        }),
        error_messages={
            'required': 'وارد کردن رمز عبور جدید الزامی است'
        }
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '*********',
            'id': 'register-password-4'
        }),
        error_messages={
            'required': 'تکرار رمز عبور الزامی است'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError('رمز عبور و تکرار آن مطابقت ندارند')
        return cleaned_data
