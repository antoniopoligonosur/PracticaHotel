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

# 5) Huéspedes
# ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE HUESPED Y SU PERFIL RELACIONADO:
# Muestra nombre, apellido, correo y telefono
def huesped_lista(request):
    huespedes = Huesped.objects.all().prefetch_related('perfil')

    '''
    huespedes = Huesped.objects.raw(" SELECT h.* FROM hotel_huesped h "
                                    " LEFT JOIN hotel_perfilhuesped ph ON ph.huesped_id = h.id "
                                    " WHERE ph.nacionalidad = 'España' ")
    '''
    return render(request, 'hotel/huesped_lista.html', {'huesped_lista': huespedes})

# 6) Perfil Huésped
# ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE PERFILHUESPED Y SU HUESPED RELACIONADO:
# Muestra huesped, nacionalidad y puntos_fidelidad
def perfil_huesped_lista(request):
    
    perfiles = PerfilHuesped.objects.select_related('huesped').all()

    '''
    perfiles = PerfilHuesped.objects.raw(" SELECT ph.* FROM hotel_perfilhuesped ph "
                                        " JOIN hotel_huesped h ON h.id = ph.huesped_id "
                                         " ORDER BY ph.puntos_fidelidad DESC ")
    ''' 
    return render(request, 'hotel/perfil_huesped_lista.html', {'perfil_lista': perfiles})

# 7) Servicios
# ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE SERVICIO:
# Muestra nombre, precio, es_opcional y duracion_minutos
def servicio_lista(request):
    
    servicios = Servicio.objects.all()

    '''
    servicios = Servicio.objects.raw(" SELECT * FROM hotel_servicio s "
                                     " WHERE s.es_opcional = true OR s.precio < 10.00 "
                                     " ORDER BY s.nombre ")
    '''
    return render(request, 'hotel/servicio_lista.html', {'servicio_lista': servicios})

# 8) Reservas
# ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE RESERVA Y SU INFORMACION RELACIONADA CON HUESPED Y HABITACION:
# Muestra id, huesped, habitacion, fecha_entrada, fecha_salida, estado y total_servicios
def reserva_lista(request):
    reservas = Reserva.objects.select_related('huesped', 'habitacion').annotate(total_servicios=Sum('servicios__precio'))

    '''
    reservas = Reserva.objects.raw(" SELECT r.id, SUM(s.precio) AS total_servicios FROM hotel_reserva r "
                                   " LEFT JOIN hotel_reservaservicio rs ON rs.reserva_id = r.id "
                                   " LEFT JOIN hotel_servicio s ON s.id = rs.servicio_id "
                                   " GROUP BY r.id ")
    '''
    return render(request, 'hotel/reserva_lista.html', {'reserva_lista': reservas})

# 9) Facturas
# ESTA VISTA SIRVE PARA MOSTRAR EL CONTENIDO DE FACTURA Y SU RESERVA RELACIONADA:
# Muestra numero_factura, reserva, emitida_en, monto_total y pagada
def factura_lista(request):
    facturas = Factura.objects.select_related('reserva', 'reserva__huesped').all()

    '''
    facturas = Factura.objects.raw(" SELECT f.* FROM hotel_factura f "
                                   " JOIN hotel_reserva r ON r.id = f.reserva_id "
                                   " ORDER BY f.emitida_en DESC ")
    '''
    return render(request, 'hotel/factura_lista.html', {'factura_lista': facturas})

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', status=404)
