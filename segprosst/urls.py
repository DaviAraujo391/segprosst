# segprosst/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('usuarios/', include('usuarios.urls')),

    # ✅ Adicione esta linha para corrigir o erro:
    path('cursos/', include('cursos.urls', namespace='cursos')),
]

# Servir arquivos estáticos/media no desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






