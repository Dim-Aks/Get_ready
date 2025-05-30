from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model


# Форма профиля пользователя в ЛК
class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    email = forms.CharField(
        disabled=True,
        label="E-mail",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email"]


# Форма регистрации
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        label="Повтор пароля", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "email": "E-mail",
        }
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-input"}),
        }

    # Проверка email на уникальность
    def clean_email(self):
        User = get_user_model()
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


# Форма смены пароля
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    new_password1 = forms.CharField(
        label="Новый пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    new_password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
    )
