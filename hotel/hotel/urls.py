from django.urls import path
from . import views

urlpatterns = [
   path('',views.index, name='index'),
   path('contacto/lista', views.contacto_lista, name='contacto_lista'),
   #path('hoteles/listar',views.listar_hoteles,name='listar_hoteles'),
]

