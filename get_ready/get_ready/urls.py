from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('meetings.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace="users")),
]

admin.site.site_header = "Панель решалы"
