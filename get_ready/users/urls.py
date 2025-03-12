from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = "users"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', TemplateView.as_view(template_name='users/register.html'), name='register'),
]