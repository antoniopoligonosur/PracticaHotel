from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum, Avg, Min, Max, Prefetch
from django.views.defaults import page_not_found
from django.db.models import Q
from .models import (
    Hotel, ContactoHotel, TipoHabitacion, Habitacion, Huesped,
    PerfilHuesped, Servicio, Reserva, Factura, ReservaServicio
)
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect

def index(request):
    return render(request, 'base/index.html')

def huesped_lista(request):
    huesped = Huesped.objects.all()
    
    return render(request, 'huespedes/huesped_lista.html', {'huesped_lista':huesped})

# 1) CONTACTO
# Muestra los contactos de los hoteles junto con la información del hotel relacionado

def contacto_lista(request):
    contacto = ContactoHotel.objects.select_related("hotel").all()
    
    '''
    contacto = ContactoHotel.objects.raw(" SELECT * FROM hotel_contactohotel ch "
                                         " JOIN hotel_hotel h ON h.id = ch.hotel_id ")
    '''
    return render(request, 'contactos/contacto_lista.html', {'contacto_lista':contacto})

# 2) HOTELES
# Muestra los hoteles con sus servicios asociados (usando "LIMIT 10" para restringir la cantidad de resultados
# y mostrar únicamente los 10 hoteles con mejor calificación).

def hotel_lista(request):
    hoteles = Hotel.objects.prefetch_related('servicios').all()


    '''
    hoteles = Hotel.objects.raw(" SELECT * FROM hotel_hotel h "
                                " ORDER BY h.calificacion DESC "
                                " LIMIT 10 ")
    '''
    return render(request, 'hoteles/hotel_lista.html', {'hotel_lista': hoteles})

# 3) TIPOS DE HABITACIÓN
# Muestra los tipos de habitación existentes, y si el huesped introduce un nombre en la URL (?nombre=suite),
# se filtran solo los que contengan ese texto.

# Explicación del uso del condicional:
# Permite reutilizar la misma vista para dos comportamientos:
# - Si el huesped busca por nombre, se aplicará un filtro
# - Si no hay filtro, se mostrarán todos los tipos de habitación.

def tipo_habitacion_lista(request):

    tipos = TipoHabitacion.objects.filter(Q(capacidad=2) | Q(precio_base__lt=50.00)).all()
    
    '''
    tipos = TipoHabitacion.objects.raw(" SELECT * FROM hotel_tipohabitacion th "
                                       " WHERE th.capacidad = 2 OR th.precio_base < 50.00 ")
    '''
    return render(request, 'tipos_habitaciones/tipo_habitacion_lista.html', {'tipo_lista': tipos})

# 4) HABITACIONES
# Muestra las habitaciones filtradas por el id del hotel recibido en la URL.
# Cada habitación incluye sus datos de tipo, hotel y servicios asociados.

# Nota: Al filtrarse por id, por defecto en la web se mostrará el hotel con id "1"
# (que solo tiene una habitación asociada). Si pruebas con el id "8", verás que devuelve dos.
    
def habitacion_lista(request, hotel_id):
    
    qs = Habitacion.objects.select_related('tipo', 'hotel').prefetch_related('servicios').filter(hotel_id=hotel_id).all()
    '''
    qs = Habitacion.objects.raw(" SELECT hb.* FROM hotel_habitacion hb "
                                        " JOIN hotel_hotel h ON h.id = hb.hotel_id "
                                        " WHERE hb.hotel_id = %s" % (hotel_id if hotel_id else 0))
    '''
    
    return render(request, 'habitaciones/habitacion_lista.html', {'habitacion_lista': qs})

# 5) HOTEL - DETALLE
# Muestra la información de un hotel específico junto con todos sus servicios.
# Se usa "prefetch"

def detalle_hotel(request, id_hotel):

    hotel = Hotel.objects.prefetch_related('servicios').filter(id=id_hotel).all()[0]
    
    return render(request, 'hoteles/detalle_hotel.html', {'hotel': hotel})

# 6) PERFIL HUÉSPED
# Muestra la lista de perfiles de huéspedes junto con la información básica del huésped relacionado.
def perfil_huesped_lista(request):
    
    perfiles = PerfilHuesped.objects.select_related('huesped').order_by('-puntos_fidelidad').all()

    '''
    perfiles = PerfilHuesped.objects.raw(" SELECT ph.* FROM hotel_perfilhuesped ph "
                                        " JOIN hotel_huesped h ON h.id = ph.huesped_id "
                                         " ORDER BY ph.puntos_fidelidad DESC ")
    ''' 
    return render(request, 'perfiles/perfil_huesped_lista.html', {'perfil_lista': perfiles})

# 7) SERVICIOS
# Muestra los servicios disponibles.
# En la versión SQL se utiliza "OR" para mostrar los servicios opcionales
# o aquellos cuyo precio sea inferior a un valor determinado.
def servicio_lista(request):
    
    servicios = Servicio.objects.filter(Q(es_opcional=True) | Q(precio__lt=10.00)).order_by('nombre').all()

    '''
    servicios = Servicio.objects.raw(" SELECT * FROM hotel_servicio s "
                                     " WHERE s.es_opcional = true OR s.precio < 10.00 "
                                     " ORDER BY s.nombre ")
    '''
    return render(request, 'servicios/servicio_lista.html', {'servicio_lista': servicios})

# 8) HOTELES POR FECHA
# Muestra los hoteles fundados en un año y mes concretos.
# Esta vista recibe 2 parámetros en la URL: "anyo_hotel" y "mes_hotel".

def dame_hotel_fecha(request, anyo_hotel, mes_hotel):
    
    hoteles = Hotel.objects.prefetch_related('servicios').filter(
        fecha_fundacion__year=anyo_hotel,
        fecha_fundacion__month=mes_hotel
    ).all()
    
    '''
    # Esta sentencia convierte el mes a cadena permitiendo que tenga 2 digitos por ejemplo: (Enero: 01)
    mes_formato_sql = str(mes_hotel).zfill(2)
    
    hoteles = (Hotel.objects.raw(
      "SELECT * FROM hotel_hotel h "
    +" WHERE strftime('%%Y', h.fecha_fundacion) = %s "
    +" AND strftime('%%m', h.fecha_fundacion) = %s "
    ,[str(anyo_hotel),mes_formato_sql]))
    '''
    
    return render(request, 'hoteles/hotel_lista.html', {'hotel_lista': hoteles})

# 9) HOTEL - CALIFICACIÓN
# Muestra los hoteles con una calificación exacta recibida por parámetro.
# Se emplea una expresión regular para comparar valores concretos.

def dame_hotel_calificacion(request, calificacion_hotel):
    
    hoteles = Hotel.objects.prefetch_related('servicios').filter(calificacion=calificacion_hotel).all()

    """
    hoteles = (Hotel.objects.raw(
    "SELECT * FROM hotel_hotel h "
    + " WHERE h.calificacion = %s "
    ,[calificacion_hotel]))
    """
    return render(request, 'hoteles/hotel_lista.html', {'hotel_lista': hoteles})

# 10) ESTADÍSTICAS DE HOTELES
# Calcula estadísticas de calificación de los hoteles (media, máxima y mínima)
# usando funciones de agregación (aggregate).

def hoteles_estadisticas_calificacion(request):
    
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
    """ 
    return render(request, 'hoteles/estadistica_hotel.html', {'estadistica': estadisticas})

def menu_enlaces(request):
    return render(request, 'base/menu_enlaces.html')

#-------- HUESPED (CREATE) --------
def huesped_create(request): # Metodo que controla el Tipo de formulario

    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST

    formulario = HuespedForm(datosFormulario)

    if (request.method == "POST"):
        
        huesped_creado = crear_huesped_modelo(formulario)
        
        if(huesped_creado):
            messages.success(request, 'Se ha creado el Huesped: [ '+formulario.cleaned_data.get('nombre')+" ] correctamente.")
            return redirect('index')

    return render(request, 'huespedes/crud/create_huesped.html',{'formulario':formulario})

def crear_huesped_modelo(formulario): # Metodo que crea en la base de datos

        huesped_creado = False
        # Comprueba si el formulario es válido
        if formulario.is_valid():
            try:
                # Guarda el huesped en la base de datos
                formulario.save()
                huesped_creado = True
            except Exception as error:
                print(error)
        return huesped_creado

#-------- HUESPED - BUSCAR AVANZADO (READ) --------

def huesped_buscar_avanzado(request): 

    if(len(request.GET) > 0):
        formulario = HuespedBuscarAvanzada(request.GET)
        if formulario.is_valid():
        
            mensaje_busqueda = 'Filtros Aplicados:\n'
            QsHuesped = Huesped.objects
            
            #Obtenemos los campos del formulario
            nombre_huesped_contiene = formulario.cleaned_data.get('nombre_huesped_contiene')
            fecha_nacimiento_desde = formulario.cleaned_data.get('fecha_nacimiento_desde')
            fecha_nacimiento_hasta = formulario.cleaned_data.get('fecha_nacimiento_hasta')
            
            #---Nombre---
            if(nombre_huesped_contiene!=''):
                nombre_huesped_contiene = nombre_huesped_contiene.strip()
                QsHuesped = QsHuesped.filter(nombre__icontains=nombre_huesped_contiene)
                mensaje_busqueda += '· Nombre contiene "'+nombre_huesped_contiene+'"\n'
            else:
                mensaje_busqueda += '· Cualquier nombre \n'
            
            #---Fecha---
            if (not fecha_nacimiento_desde is None):
                QsHuesped = QsHuesped.filter(fecha_nacimiento__gte=fecha_nacimiento_desde)
                mensaje_busqueda += '· nacimiento desde '+datetime.strftime(fecha_nacimiento_desde,'%d-%m-%Y')+'\n'
            else:
                mensaje_busqueda += '· nacimiento desde: Cualquier fecha \n'
            
            if (not fecha_nacimiento_hasta is None):
                QsHuesped = QsHuesped.filter(fecha_nacimiento__lte=fecha_nacimiento_hasta)
                mensaje_busqueda += '· nacimiento hasta '+datetime.strftime(fecha_nacimiento_hasta,'%d-%m-%Y')+'\n'
            else:
                mensaje_busqueda += '· nacimiento hasta: Cualquier fecha \n'

            #Ejecutamos la querySet y enviamos los HQsHuesped
            huespedes = QsHuesped.all()
            
            return render(request, 'huespedes/huesped_lista.html',
                        {'huesped_lista':huespedes,
                        'Mensaje_Busqueda':mensaje_busqueda}
                        )
    else:
        formulario = HuespedBuscarAvanzada(None)
    return render(request, 'huespedes/crud/buscar_avanzada_huespedes.html',{'formulario':formulario})

#--------- HUESPED EDITAR

def huesped_editar(request, id_huesped): 

    huesped = Huesped.objects.get(id=id_huesped)

    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST

    formulario = HuespedForm(datosFormulario, instance=huesped)

    if (request.method == "POST"):
        
        huesped_creado = crear_huesped_modelo(formulario)
        
        if(huesped_creado):
            messages.success(request, 'Se ha editado el Huesped: [ '+formulario.cleaned_data.get('nombre')+" ] correctamente.")
            return redirect('index')

    return render(request, 'huespedes/crud/actualizar_huesped.html',{'formulario':formulario, 'huesped':huesped})

#-------- HUESPED ELIMINAR

def huesped_eliminar(request, id_huesped):
    huesped = Huesped.objects.get(id=id_huesped)
    try:
        huesped.delete()
    except:
        pass
    return redirect('huesped_lista')

# Error 404 - Página no encontrada
def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', None,None,404)

# Error 500 - Error interno del servidor
def mi_error_500(request):
    return render(request, 'errores/500.html', status=500)

# Error 403 - Acceso prohibido
def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html', status=403)

# Error 400 - Solicitud incorrecta
def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html', status=400)
