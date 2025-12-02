from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
   path('',views.index, name='index'),
   # 2) Hotel
   path('hotel/lista', views.hotel_lista, name='hotel_lista'),
   # 3) Tipo Habitacion
   path('tipohabitacion/lista', views.tipo_habitacion_lista, name='tipo_habitacion'),
   # 4) Habitacion
   path('habitacion/lista/<int:hotel_id>/', views.habitacion_lista, name='habitacion_lista'),
   # 5) HOTEL - DETALLE
   path('detalles_hotel/<int:id_hotel>/', views.detalle_hotel, name='detalle_hotel'),
   # 7) Servicio
   path('servicio/lista', views.servicio_lista, name='servicio_lista'),
   # 8) HOTELES POR FECHA
   path('hotel/lista/<int:anyo_hotel>/<int:mes_hotel>', views.dame_hotel_fecha, name="dame_hotel_fecha"),
   # 9) Hotel - Calificacion - Expresion Regular
   re_path(r'^hotel/calificacion/(?P<calificacion_hotel>0\.\d{2})/$', views.dame_hotel_calificacion, name='dame_hotel_calificacion'),
   # 10) ESTADÍSTICAS DE HOTELES - Agreggate
   path('hoteles/estadisticas_calificacion/', views.hoteles_estadisticas_calificacion, name='hoteles_estadisticas_calificacion'),
   # 11) Huesped - Crear Huesped
   path('huesped/crear', views.huesped_create, name='huesped_create'),
   # 12) Huesped - Buscar Huesped Avanzada
   path('huesped/buscar/avanzado/',views.huesped_buscar_avanzado, name='huesped_buscar_avanzado'),
   path('menu-enlaces/',views.menu_enlaces, name='menu_enlaces'),
   path('huesped/editar/<int:id_huesped>',views.huesped_editar, name='huesped_editar'),
   path('huesped/eliminar/<int:id_huesped>',views.huesped_eliminar, name='huesped_eliminar'),
   path('huesped/listar/',views.huesped_lista, name='huesped_lista'),
   path('huesped/listar/',views.huesped_lista, name='huesped_lista'),

   # -----------------------------------------------------------------------------
   # HOTEL CRUD
   # -----------------------------------------------------------------------------
   path('hotel/crear', views.hotel_create, name='hotel_create'),
   path('hotel/editar/<int:id_hotel>', views.hotel_editar, name='hotel_editar'),
   path('hotel/eliminar/<int:id_hotel>', views.hotel_eliminar, name='hotel_eliminar'),
   path('hotel/buscar/avanzado/', views.hotel_buscar_avanzado, name='hotel_buscar_avanzado'),




    path('habitaciones/fotos/', views.fotos_habitaciones, name='fotos_habitaciones'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
