from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve
from ai import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_image, name='home'),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
