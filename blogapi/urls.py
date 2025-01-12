from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from blogapi import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('blogs/', include('blogs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
