from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
   path('',views.index, name='index'),
   # 1) Contacto
   path('contacto/lista', views.contacto_lista, name='contacto_lista'),
   # 2) Hotel
   path('hotel/lista', views.hotel_lista, name='hotel_lista'),
   # 3) Tipo Habitacion
   path('tipohabitacion/lista', views.tipo_habitacion_lista, name='tipo_habitacion'),
   # 4) Habitacion
   path('habitacion/lista/<int:hotel_id>/', views.habitacion_lista, name='habitacion_lista'),
   # 5) HOTEL - DETALLE
   path('detalles_hotel/<int:id_hotel>/', views.detalle_hotel, name='detalle_hotel'),
   # 6) Perfil Huesped
   path('perfil_huesped/lista', views.perfil_huesped_lista, name='perfil_huesped_lista'),
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

   # -----------------------------------------------------------------------------
   # CONTACTO CRUD
   # -----------------------------------------------------------------------------
   path('contacto/crear', views.contacto_create, name='contacto_create'),
   path('contacto/editar/<int:id_contacto>', views.contacto_editar, name='contacto_editar'),
   path('contacto/eliminar/<int:id_contacto>', views.contacto_eliminar, name='contacto_eliminar'),
   path('contacto/buscar/avanzado/', views.contacto_buscar_avanzado, name='contacto_buscar_avanzado'),

   # -----------------------------------------------------------------------------
   # PERFIL HUESPED CRUD
   # -----------------------------------------------------------------------------
   path('perfil_huesped/crear', views.perfil_huesped_create, name='perfil_huesped_create'),
   path('perfil_huesped/editar/<int:id_perfil>', views.perfil_huesped_editar, name='perfil_huesped_editar'),
   path('perfil_huesped/eliminar/<int:id_perfil>', views.perfil_huesped_eliminar, name='perfil_huesped_eliminar'),
   path('perfil_huesped/buscar/avanzado/', views.perfil_huesped_buscar_avanzado, name='perfil_huesped_buscar_avanzado'),

   # -----------------------------------------------------------------------------
   # RESERVA CRUD
   # -----------------------------------------------------------------------------
   path('reserva/lista', views.reserva_lista, name='reserva_lista'),
   path('reserva/crear', views.reserva_create, name='reserva_create'),
   path('reserva/editar/<int:id_reserva>', views.reserva_editar, name='reserva_editar'),
   path('reserva/eliminar/<int:id_reserva>', views.reserva_eliminar, name='reserva_eliminar'),
   path('reserva/buscar/avanzado/', views.reserva_buscar_avanzado, name='reserva_buscar_avanzado'),

   # -----------------------------------------------------------------------------
   # FACTURA CRUD
   # -----------------------------------------------------------------------------
    path('factura/lista', views.factura_lista, name='factura_lista'),
    path('factura/crear', views.factura_create, name='factura_create'),
    path('factura/editar/<int:id_factura>', views.factura_editar, name='factura_editar'),
    path('factura/eliminar/<int:id_factura>', views.factura_eliminar, name='factura_eliminar'),
    path('factura/buscar/avanzado/', views.factura_buscar_avanzado, name='factura_buscar_avanzado'),
    path('factura/buscar/avanzado/', views.factura_buscar_avanzado, name='factura_buscar_avanzado'),
    
    # -----------------------------------------------------------------------------
    # GESTIÓN DE IMÁGENES
    # -----------------------------------------------------------------------------
    path('hotel/imagenes/', views.gestion_imagenes, name='gestion_imagenes'),
]




