from django.shortcuts import render
from .models import Hotel
# from django.views.defaults import page_not_found   # no necesario aquí

def index(request):
    return render(request, 'hotel/index.html')

def listar_hoteles(request):
    #hoteles = Hotel.objects.prefetch_related("servicios").all()

    
    hoteles = Hotel.objects.raw("SELECT * FROM hotel_hotel h"
                             " JOIN hotel_hotel_servicios hs ON hs.hotel_id = h.id")
    
    return render(request, 'hotel/hotel.html', {"hoteles_mostrar": hoteles})

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', status=404)
