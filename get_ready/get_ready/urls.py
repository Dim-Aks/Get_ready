from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('meetings/', include('meetings.urls')),
    path('admin/', admin.site.urls),
]
