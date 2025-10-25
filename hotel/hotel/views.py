from django.shortcuts import render
from .models import Hotel, ContactoHotel

def index(request):
    return render(request, 'hotel/index.html')

#ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE CONTACTO Y SU INFORMACIÓN RELACIONADA CON HOTEL:
# Muestra nombre_contacto, telefono, correo, sitio_web y hotel.

def contacto_lista(request):
    contacto = ContactoHotel.objects.select_related("hotel")
    
    '''
    contacto = ContactoHotel.objects.raw(" SELECT * FROM hotel_contactohotel ch "
                                         " JOIN hotel_hotel h ON h.id = ch.hotel_id ")
    '''
    return render(request, 'hotel/contacto_lista.html', {'contacto_lista':contacto})

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', status=404)
