from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
if settings.DEBUG:
    urlpatterns += path('', include_docs_urls(title='Aichrom API')),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
