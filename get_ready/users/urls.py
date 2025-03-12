from django.urls import path
from .views import logout_user, LoginUser
from django.views.generic.base import TemplateView

app_name = "users"

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', TemplateView.as_view(template_name='users/register.html'), name='register'),
]