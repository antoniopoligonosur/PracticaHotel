from django.urls import path
from . import views

urlpatterns = [
   path('',views.index, name='index'),
   path('hoteles/listar',views.listar_hoteles,name='listar_hoteles'),
]

