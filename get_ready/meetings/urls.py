from django.urls import path
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='meetings/index.html', extra_context={'title': "Собирайся!"}), name='home'),
    path('suggest/', views.create_suggest, name='suggest'),
    path('check/', views.view_meetings, name='check'),
    path('check/<int:pk>/', views.meeting_detail, name='meeting_detail'),
    path('edit/<int:pk>/', views.UpdateMeeting.as_view(), name='edit_page'),
]