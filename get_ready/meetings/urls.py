from django.urls import path
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='meetings/index.html'), name='home'),
    path('suggest/', views.create_suggest, name='suggest'),
    path('check/', TemplateView.as_view(template_name='meetings/check.html'), name='check'),
]