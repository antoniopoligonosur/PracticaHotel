from django.shortcuts import render
from .models import Hotel, ContactoHotel

def index(request):
    return render(request, 'hotel/index.html')

# 1) Contacto
# ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE CONTACTO Y SU INFORMACIÓN RELACIONADA CON HOTEL:
# Muestra nombre_contacto, telefono, correo, sitio_web y hotel.

def contacto_lista(request):
    contacto = ContactoHotel.objects.select_related("hotel")
    
    '''
    contacto = ContactoHotel.objects.raw(" SELECT * FROM hotel_contactohotel ch "
                                         " JOIN hotel_hotel h ON h.id = ch.hotel_id ")
    '''
    return render(request, 'hotel/contacto_lista.html', {'contacto_lista':contacto})

# 2) Hoteles
# ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE HOTEL Y SU INFORMACION RELACIONADA CON SERVICIOS:
# Muestra nombre, descripcion, direccion, calificacion y num_habitaciones

def hotel_lista(request):
    hoteles = Hotel.objects.prefetch_related('servicios').all()

    '''
    hoteles = Hotel.objects.raw(" SELECT * FROM hotel_hotel h "
                                " ORDER BY h.calificacion DESC "
                                " LIMIT 10 ")
    '''
    return render(request, 'hotel/hotel_lista.html', {'hotel_lista': hoteles})

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', status=404)
