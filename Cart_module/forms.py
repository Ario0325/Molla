from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        label='نام',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خود را وارد کنید',
            'required': True,
            'id': 'first_name'
        })
    )

    last_name = forms.CharField(
        max_length=100,
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی خود را وارد کنید',
            'required': True,
            'id': 'last_name'
        })
    )

    address = forms.CharField(
        label='آدرس',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'آدرس کامل خود را وارد کنید',
            'required': True,
            'id': 'address'
        })
    )

    postal_code = forms.CharField(
        max_length=10,
        label='کد پستی',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کد پستی خود را وارد کنید',
            'required': True,
            'id': 'postal_code'
        })
    )

    phone = forms.CharField(
        max_length=11,
        label='شماره تماس',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره موبایل خود را وارد کنید',
            'required': True,
            'id': 'phone',
            'pattern': '09[0-9]{9}'
        })
    )

    description = forms.CharField(
        required=False,
        label='توضیحات سفارش',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'توضیحات اضافی در مورد سفارش',
            'id': 'description'
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone) != 11 or not phone.startswith('09'):
            raise forms.ValidationError('لطفا یک شماره موبایل معتبر وارد کنید')
        return phone

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if not postal_code.isdigit() or len(postal_code) != 10:
            raise forms.ValidationError('لطفا یک کد پستی معتبر 10 رقمی وارد کنید')
        return postal_code

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name.strip()) < 2:
            raise forms.ValidationError('نام باید حداقل 2 کاراکتر باشد')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name.strip()) < 2:
            raise forms.ValidationError('نام خانوادگی باید حداقل 2 کاراکتر باشد')
        return last_name

    def clean_address(self):
        address = self.cleaned_data['address']
        if len(address.strip()) < 10:
            raise forms.ValidationError('لطفا آدرس کامل را وارد کنید')
        return address
