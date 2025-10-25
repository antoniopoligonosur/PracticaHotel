from django.shortcuts import render
from django.db.models import Sum
from .models import (
    Hotel, ContactoHotel, TipoHabitacion, Habitacion, Huesped,
    PerfilHuesped, Servicio, Reserva, Factura, ReservaServicio
)

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

# 3) Tipos de Habitación
# ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE TIPOHABITACION:
# Muestra nombre, capacidad y precio_base

# En esta vista se utiliza un condicional (if) porque queremos que la misma ruta sirva
# tanto para mostrar todas las habitaciones como para filtrar por nombre cuando el usuario lo indique.

# 1. Se usa request.GET.get('nombre') para obtener el parámetro opcional "nombre"
#    desde la URL (por ejemplo: /tipohabitacion/lista?nombre=suite).

# 2. Si el parámetro "nombre" tiene un valor, se aplica un filtro con filter(nombre__icontains=nombre)
#    para mostrar solo los tipos de habitación cuyo nombre contenga ese texto.

# 3. Si no se pasa ningún valor, se ejecuta TipoHabitacion.objects.all()
#    para mostrar todos los registros disponibles.

def tipo_habitacion_lista(request):
    nombre = request.GET.get('nombre')  # Obtiene el nombre desde la URL
    if nombre:
        tipos = TipoHabitacion.objects.filter(nombre__icontains=nombre)
    else:
        tipos = TipoHabitacion.objects.all()
    
    '''
    tipos = TipoHabitacion.objects.raw(" SELECT * FROM hotel_tipohabitacion th "
                                       " WHERE th.capacidad = 2 OR th.precio_base < 50.00 ")
    '''
    return render(request, 'hotel/tipo_habitacion_lista.html', {'tipo_lista': tipos})

# 4) Habitaciones
# ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE HABITACION Y SU INFORMACION RELACIONADA CON TIPO Y HOTEL:
# Muestra hotel, número, piso, tipo y disponible.

# Si se recibe un parámetro hotel_id en la URL, se filtran las habitaciones
# para mostrar solo las que pertenecen a ese hotel. 
# Si no se recibe, se muestran todas las habitaciones.

def habitacion_lista(request, hotel_id=None):
    
    qs = Habitacion.objects.select_related('tipo', 'hotel').prefetch_related('servicios')
    if hotel_id is not None:
        qs = qs.filter(hotel_id=hotel_id)
    
    '''
    habitacion = Habitacion.objects.raw(" SELECT hb.* FROM hotel_habitacion hb "
                                        " JOIN hotel_hotel h ON h.id = hb.hotel_id "
                                        " WHERE hb.hotel_id = %s" % (hotel_id if hotel_id else 0))
    '''
    
    return render(request, 'hotel/habitacion_lista.html', {'habitacion_lista': qs})

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', status=404)
