from django.shortcuts import render
from django.db.models import Sum, Avg, Min, Max, Prefetch
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

# Al filtrarse con id, en la web por defecto te mostrará la id "1" la cual solo tiene asociada una habitacion, y si pruebas
# por ejemplo el id "8" te saldrán 2

def habitacion_lista(request, hotel_id):
    
    qs = Habitacion.objects.select_related('tipo', 'hotel').prefetch_related('servicios').filter(hotel_id=hotel_id)
    qs.all()
    '''
    qs = Habitacion.objects.raw(" SELECT hb.* FROM hotel_habitacion hb "
                                        " JOIN hotel_hotel h ON h.id = hb.hotel_id "
                                        " WHERE hb.hotel_id = %s" % (hotel_id if hotel_id else 0))
    '''
    
    return render(request, 'hotel/habitacion_lista.html', {'habitacion_lista': qs})

# 5) Hotel - Detalle
def detalle_hotel(request, id_hotel):
    hotel = Hotel.objects.prefetch_related(
        Prefetch('servicios')
    ).get(id=id_hotel)
    
    return render(request, 'hotel/detalle_hotel.html', {'hotel': hotel})

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

def dame_hotel_fecha(request, anyo_hotel, mes_hotel):
    
    hoteles = Hotel.objects.prefetch_related('servicios').filter(fecha_fundacion__year=anyo_hotel, fecha_fundacion__month=mes_hotel)
    
    '''
    # Esta sentencia convierte el mes a cadena permitiendo que tenga 2 digitos por ejemplo: (Enero: 01)
    mes_formato_sql = str(mes_hotel).zfill(2)
    
    hoteles = (Hotel.objects.raw(
      "SELECT * FROM hotel_hotel h "
    +" WHERE strftime('%%Y', h.fecha_fundacion) = %s "
    +" AND strftime('%%m', h.fecha_fundacion) = %s "
    ,[str(anyo_hotel),mes_formato_sql]))
    '''
    
    return render(request, 'hotel/hotel_lista.html', {'hotel_lista': hoteles})

# 9) Hotel - Calificacion

def dame_hotel_calificacion(request, calificacion_hotel):
    
    hoteles = Hotel.objects.prefetch_related('servicios').filter(calificacion=calificacion_hotel)

    """
    hoteles = (Hotel.objects.raw(
    "SELECT * FROM hotel_hotel h "
    + " WHERE h.calificacion = %s "
    ,[calificacion_hotel]))
    """
    return render(request, 'hotel/hotel_lista.html', {'hotel_lista': hoteles})

# 10) Hotel - Calificacion - Agreggate

def hoteles_estadisticas_calificacion(request):
    """
    estadisticas = (
    Hotel.objects
    .aggregate(
            media_calificacion=Avg('calificacion'),
            max_calificacion=Max('calificacion'),
            min_calificacion=Min('calificacion')
    )
    )
    """
     
    estadisticas = (Hotel.objects.raw(
    "SELECT 1 AS id, AVG(calificacion) AS media_calificacion, MAX(calificacion) AS max_calificacion, MIN(calificacion) AS min_calificacion FROM hotel_hotel ")[0])
     
    return render(request, 'hotel/estadistica_hotel.html', {'estadistica': estadisticas})

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', None,None,404)
