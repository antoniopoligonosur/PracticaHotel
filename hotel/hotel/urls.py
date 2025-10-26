from django.urls import path
from . import views

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
   # 5) Huesped
   path('huesped/lista', views.huesped_lista, name='huesped_lista'),
   # 6) Perfil Huesped
   path('perfil_huesped/lista', views.perfil_huesped_lista, name='perfil_huesped_lista'),
   # 7) Servicio
   path('servicio/lista', views.servicio_lista, name='servicio_lista'),

]
