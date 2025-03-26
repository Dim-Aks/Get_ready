from django.urls import path
from django.views.generic.base import TemplateView
from .views import UpdateMeeting, meeting_detail, view_meetings, MeetingCreateView, DeleteMeeting

urlpatterns = [
    path('', TemplateView.as_view(template_name='meetings/index.html', extra_context={'title': "Собирайся!"}), name='home'),
    path('suggest/', MeetingCreateView.as_view(), name='suggest'),
    path('check/', view_meetings, name='check'),
    path('check/<int:pk>/', meeting_detail, name='meeting_detail'),
    path('edit/<int:pk>/', UpdateMeeting.as_view(), name='edit_page'),
    path('check/<int:pk>/delete', DeleteMeeting.as_view(), name='meeting_delete')
]