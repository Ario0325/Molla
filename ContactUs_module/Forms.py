from django import forms

from .models import ContactUs


class ContactUsModuleFrom(forms.ModelForm):
    username = forms.CharField(
        label='نام و نام خانوادگی',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "نام خود را وارد کنید ",
                'id': 'cname'
            }
        )
    )

    email = forms.EmailField(
        label='ادرس الکترونیکی',
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': "ایمیل خود را وارد کنید",
                'id': 'cemail'
            }
        )
    )

    phone = forms.CharField(
        label='شماره تماس',
        max_length=12,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "شماره موبایل خود را وارد کنید",
                'id': 'cphone'
            }
        )
    )
    object = forms.CharField(
        label='موضوع پیام شما',
        max_length=120,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "موضوع پیام شما",
                'id': 'csubject'
            }
        )
    )

    text = forms.CharField(
        label='توضیحات',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': "متن پبام",
                'id': 'cmessage'
            }
        )
    )

    class Meta:
        model = ContactUs
        fields = ['username', 'email', 'phone','object', 'text']
