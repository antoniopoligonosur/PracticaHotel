from django.urls import path
from . import views

urlpatterns = [
   path('',views.index, name='index'),
   # 1) Contacto
   path('contacto/lista', views.contacto_lista, name='contacto_lista'),
   # 2) Hotel
    path('hotel/lista', views.hotel_lista, name='hotel_lista'),
]

