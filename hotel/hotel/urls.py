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
   # ^ y $  → indican el inicio y fin de la cadena, para asegurar coincidencia exacta.
   # 0\.    → el valor debe comenzar con el número 0 seguido de un punto decimal literal.
   # \d{2}  → deben seguir exactamente dos dígitos del 0 al 9.
   # (?P<calificacion_hotel>...) → nombra la parte capturada como calificacion_hotel.
   re_path(r'^hotel/calificacion/(?P<calificacion_hotel>0\.\d{2})/$', views.dame_hotel_calificacion, name='dame_hotel_calificacion'),
   # 10) ESTADÍSTICAS DE HOTELES - Agreggate
   path('hoteles/estadisticas_calificacion/', views.hoteles_estadisticas_calificacion, name='hoteles_estadisticas_calificacion'),

]
