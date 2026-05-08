from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('envios.urls')), # Conecta con las rutas de tu app envios
    path('accounts/', include('django.contrib.auth.urls')), # Rutas de login automáticas
]

# Esto permite que Django sirva las imágenes y el CSS durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)