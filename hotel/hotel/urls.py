from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
   path('',views.index, name='index'),
   # 11) Huesped - Crear Huesped
   path('huesped/crear', views.huesped_create, name='huesped_create'),
   # 12) Huesped - Buscar Huesped Avanzada
   path('huesped/buscar/avanzado/',views.huesped_buscar_avanzado, name='huesped_buscar_avanzado'),
   path('menu-enlaces/',views.menu_enlaces, name='menu_enlaces'),
   path('huesped/editar/<int:id_huesped>',views.huesped_editar, name='huesped_editar'),
   path('huesped/eliminar/<int:id_huesped>',views.huesped_eliminar, name='huesped_eliminar'),
   path('huesped/listar/',views.huesped_lista, name='huesped_lista'),
   path('huesped/listar/',views.huesped_lista, name='huesped_lista'),





]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
