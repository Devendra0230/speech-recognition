from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from main_app import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main_app.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
