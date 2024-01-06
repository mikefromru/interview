from django.contrib import admin
from django.urls import path, include, re_path
from app.routers.api import api_urlpatterns
# from app.routers.urls import urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/app/', include(api_urlpatterns)),
    path('myadmin/', include('app.routers.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
