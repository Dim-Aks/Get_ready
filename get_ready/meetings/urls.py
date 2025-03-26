from django.urls import path
from django.views.generic.base import TemplateView
from .views import UpdateMeeting, meeting_detail, MeetingListView, MeetingCreateView, DeleteMeeting

urlpatterns = [
    path('', TemplateView.as_view(template_name='meetings/index.html', extra_context={'title': "Собирайся!"}), name='home'),
    path('suggest/', MeetingCreateView.as_view(), name='suggest'),
    path('check/', MeetingListView.as_view(), name='check'),
    path('check/<int:pk>/', meeting_detail, name='meeting_detail'),
    path('check/<int:pk>/edit/', UpdateMeeting.as_view(), name='edit_page'),
    path('check/<int:pk>/delete', DeleteMeeting.as_view(), name='meeting_delete')
]