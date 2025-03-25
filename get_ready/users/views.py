from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from .forms import RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from django.views.generic import CreateView, UpdateView


# Профиль пользователя
class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user


# Авторизация
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


# Регистрация
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


# Выход из учётки
def logout_user(request):
    logout(request)
    return redirect('home')


# Изменение пароля
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change.html"
    extra_context = {'title': "Изменение пароля"}