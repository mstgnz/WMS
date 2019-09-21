from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.EmailField(max_length=100, label="E-Mail")
    password = forms.CharField(max_length=100, label="Şifre", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Kullanıcı adını veya şifreyi yanlış girdiniz!")
        return super(LoginForm, self).clean()


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'image'
        )


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name','last_name','email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("E-Mail zaten kayıtlı")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Paralolar Eşleşmiyor")
        return password2


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'image',
            'is_active'
        )
