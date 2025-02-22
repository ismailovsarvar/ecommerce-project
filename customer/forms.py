from django import forms

from customer.models import Customer, User


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()


class LoginForm(forms.Form):
    email = forms.EmailField()
    # phone = forms.CharField(max_length=13)
    password = forms.CharField(max_length=255)

    def clean_email(self):
        email = self.data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email does not exist')
        return email

    # def clean_phone(self):
    #     phone = self.data.get('phone')
    #     if not User.objects.filter(phone=phone).exists():
    #         raise forms.ValidationError('Number does not exist')
    #     return phone

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.data.get('password')
        try:
            user = User.objects.get(email=email)
            print(user)
            if not user.check_password(password):
                raise forms.ValidationError('Password did not match')
        except User.DoesNotExist:
            raise forms.ValidationError(f'{email} does not exists')
        return password


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'The {email} email is already registered')
        return email

    def clean(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords did not match')
        return password


# class RegisterModelForm(forms.ModelForm):
#     confirm_password = forms.CharField(max_length=255)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')
#
#     def clean_email(self):
#         email = self.data.get('email').lower()
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError(f'The {email} email is already registered')
#         return email
#
#     def clean_password(self):
#         password = self.data.get('password')
#         confirm_password = self.data.get('confirm_password')
#         if password != confirm_password:
#             raise forms.ValidationError('Passwords did not match')
#         return password


class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ()
