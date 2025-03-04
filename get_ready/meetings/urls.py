from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('suggest/', views.create_suggest, name='suggest'),
    path('check/', views.check, name='check'),
]