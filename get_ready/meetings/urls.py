from django.urls import path
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='meetings/index.html'), name='home'),
    path('suggest/', views.create_suggest, name='suggest'),
    path('check/', views.view_meetings, name='check'),
    path('check/<int:pk>/', views.meeting_detail, name='meeting_detail'),
]