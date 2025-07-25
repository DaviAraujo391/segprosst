from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cursos/', include('cursos.urls')),
    path('usuarios/', include('usuarios.urls')),
    
    # Use esta linha COM namespace, se documentos/urls.py tiver app_name definido:
    path('documentos/', include(('documentos.urls', 'documentos'), namespace='documentos')),
    
    path('epi/', include('epi.urls')),
]

# Servir arquivos de mídia em modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




