from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('meetings.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace="users")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Панель решалы"
