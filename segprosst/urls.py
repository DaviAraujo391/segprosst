# segprosst/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),  # inclui core com namespace
    path('usuarios/', include('usuarios.urls')),
    path('cursos/', include('cursos.urls', namespace='cursos')),
    path('epi/', include('epi.urls', namespace='epi')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






