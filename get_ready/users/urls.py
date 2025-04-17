from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path

from .views import RegisterUser, logout_user, LoginUser, ProfileUser, UserPasswordChange

app_name = "users"

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("profile/", ProfileUser.as_view(), name="profile"),
    path(
        "password-change/done/",
        PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password_change_done",
    ),
    path("password-change/", UserPasswordChange.as_view(), name="password_change"),
]
