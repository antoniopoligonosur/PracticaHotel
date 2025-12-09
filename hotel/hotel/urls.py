from django.urls import path
from . import views
from django.urls import re_path
from django.urls import include

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
   path('registrar/', views.registrar_usuario, name='registrar_usuario'),
   path('accounts/', include('django.contrib.auth.urls')),  # Agrega las URL de autenticación de Django
   
   path('registrar',views.registrar_usuario,name='registrar_usuario'),
]
