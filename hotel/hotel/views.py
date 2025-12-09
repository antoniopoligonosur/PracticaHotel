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
    
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
    
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

# ==============================================================================
#  HELPER FUNCTIONS (GENERIC-LIKE)
# ==============================================================================

def crear_modelo_generico(formulario):
    """
    Helper genérico para guardar un formulario si es válido.
    Retorna True si se guardó correctamente, False en caso contrario.
    """
    creado = False
    if formulario.is_valid():
        try:
            formulario.save()
            creado = True
        except Exception as error:
            print(f"Error guardando modelo: {error}")
    return creado

# ==============================================================================
#  HOTEL CRUD
# ==============================================================================

def hotel_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = HotelForm(datosFormulario)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, f'Se ha creado el Hotel: [{formulario.cleaned_data.get("nombre")}] correctamente.')
            return redirect('hotel_lista')
            
    return render(request, 'hoteles/crud/create_hotel.html', {'formulario': formulario})

def hotel_editar(request, id_hotel):
    hotel = Hotel.objects.get(id=id_hotel)
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = HotelForm(datosFormulario, instance=hotel)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, f'Se ha editado el Hotel: [{formulario.cleaned_data.get("nombre")}] correctamente.')
            return redirect('hotel_lista')

    return render(request, 'hoteles/crud/actualizar_hotel.html', {'formulario': formulario, 'hotel': hotel})

def hotel_eliminar(request, id_hotel):
    hotel = Hotel.objects.get(id=id_hotel)
    try:
        hotel.delete()
        messages.success(request, "Hotel eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el hotel: {e}")
    return redirect('hotel_lista')

def hotel_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = HotelBuscarAvanzada(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Filtros Aplicados:\n'
            qs = Hotel.objects.prefetch_related('servicios')
            
            nombre_contiene = formulario.cleaned_data.get('nombre_contiene')
            calificacion_minima = formulario.cleaned_data.get('calificacion_minima')
            tiene_restaurante = formulario.cleaned_data.get('tiene_restaurante')
            
            if nombre_contiene:
                qs = qs.filter(nombre__icontains=nombre_contiene)
                mensaje_busqueda += f'· Nombre contiene "{nombre_contiene}"\n'
            
            if calificacion_minima is not None:
                qs = qs.filter(calificacion__gte=calificacion_minima)
                mensaje_busqueda += f'· Calificación >= {calificacion_minima}\n'
            
            if tiene_restaurante is not None:
                qs = qs.filter(tiene_restaurante=tiene_restaurante)
                mensaje_busqueda += f'· Restaurante: {"Sí" if tiene_restaurante else "No"}\n'
            
            hoteles = qs.all()
            return render(request, 'hoteles/hotel_lista.html', {
                'hotel_lista': hoteles,
                'Mensaje_Busqueda': mensaje_busqueda
            })
    else:
        formulario = HotelBuscarAvanzada(None)
        
    return render(request, 'hoteles/crud/buscar_avanzada_hotel.html', {'formulario': formulario})

# ==============================================================================
#  CONTACTO HOTEL CRUD
# ==============================================================================

def contacto_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = ContactoHotelForm(datosFormulario)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, f'Se ha creado el Contacto: [{formulario.cleaned_data.get("nombre_contacto")}] correctamente.')
            return redirect('contacto_lista')
            
    return render(request, 'contactos/crud/create_contacto.html', {'formulario': formulario})

def contacto_editar(request, id_contacto):
    contacto = ContactoHotel.objects.get(id=id_contacto)
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = ContactoHotelForm(datosFormulario, instance=contacto)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, f'Se ha editado el Contacto: [{formulario.cleaned_data.get("nombre_contacto")}] correctamente.')
            return redirect('contacto_lista')

    return render(request, 'contactos/crud/actualizar_contacto.html', {'formulario': formulario, 'contacto': contacto})

def contacto_eliminar(request, id_contacto):
    contacto = ContactoHotel.objects.get(id=id_contacto)
    try:
        contacto.delete()
        messages.success(request, "Contacto eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el contacto: {e}")
    return redirect('contacto_lista')

def contacto_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = ContactoHotelBuscarAvanzada(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Filtros Aplicados:\n'
            qs = ContactoHotel.objects.select_related("hotel")
            
            nombre_contacto_contiene = formulario.cleaned_data.get('nombre_contacto_contiene')
            correo_contiene = formulario.cleaned_data.get('correo_contiene')
            
            if nombre_contacto_contiene:
                qs = qs.filter(nombre_contacto__icontains=nombre_contacto_contiene)
                mensaje_busqueda += f'· Nombre contiene "{nombre_contacto_contiene}"\n'
            
            if correo_contiene:
                qs = qs.filter(correo__icontains=correo_contiene)
                mensaje_busqueda += f'· Correo contiene "{correo_contiene}"\n'
            
            contactos = qs.all()
            return render(request, 'contactos/contacto_lista.html', {
                'contacto_lista': contactos,
                'Mensaje_Busqueda': mensaje_busqueda
            })
    else:
        formulario = ContactoHotelBuscarAvanzada(None)
        
    return render(request, 'contactos/crud/buscar_avanzada_contacto.html', {'formulario': formulario})

# ==============================================================================
#  PERFIL HUESPED CRUD
# ==============================================================================

def perfil_huesped_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = PerfilHuespedForm(datosFormulario)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, 'Se ha creado el Perfil de Huésped correctamente.')
            return redirect('perfil_huesped_lista')
            
    return render(request, 'perfiles/crud/create_perfil_huesped.html', {'formulario': formulario})

def perfil_huesped_editar(request, id_perfil):
    perfil = PerfilHuesped.objects.get(id=id_perfil)
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = PerfilHuespedForm(datosFormulario, instance=perfil)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, 'Se ha editado el Perfil de Huésped correctamente.')
            return redirect('perfil_huesped_lista')

    return render(request, 'perfiles/crud/actualizar_perfil_huesped.html', {'formulario': formulario, 'perfil': perfil})

def perfil_huesped_eliminar(request, id_perfil):
    perfil = PerfilHuesped.objects.get(id=id_perfil)
    try:
        perfil.delete()
        messages.success(request, "Perfil eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el perfil: {e}")
    return redirect('perfil_huesped_lista')

def perfil_huesped_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = PerfilHuespedBuscarAvanzada(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Filtros Aplicados:\n'
            qs = PerfilHuesped.objects.select_related('huesped')
            
            nacionalidad_contiene = formulario.cleaned_data.get('nacionalidad_contiene')
            puntos_minimos = formulario.cleaned_data.get('puntos_minimos')
            
            if nacionalidad_contiene:
                qs = qs.filter(nacionalidad__icontains=nacionalidad_contiene)
                mensaje_busqueda += f'· Nacionalidad contiene "{nacionalidad_contiene}"\n'
            
            if puntos_minimos is not None:
                qs = qs.filter(puntos_fidelidad__gte=puntos_minimos)
                mensaje_busqueda += f'· Puntos >= {puntos_minimos}\n'
            
            perfiles = qs.all()
            return render(request, 'perfiles/perfil_huesped_lista.html', {
                'perfil_lista': perfiles,
                'Mensaje_Busqueda': mensaje_busqueda
            })
    else:
        formulario = PerfilHuespedBuscarAvanzada(None)
        
    return render(request, 'perfiles/crud/buscar_avanzada_perfil_huesped.html', {'formulario': formulario})


# ==============================================================================
#  RESERVA CRUD
# ==============================================================================

def reserva_lista(request):
    reservas = Reserva.objects.select_related('huesped', 'habitacion').all()
    return render(request, 'reservas/reserva_lista.html', {'reserva_lista': reservas})

def reserva_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = ReservaForm(datosFormulario)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, 'Se ha creado la Reserva correctamente.')
            return redirect('reserva_lista')
            
    return render(request, 'reservas/crud/create_reserva.html', {'formulario': formulario})

def reserva_editar(request, id_reserva):
    reserva = Reserva.objects.get(id=id_reserva)
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = ReservaForm(datosFormulario, instance=reserva)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, 'Se ha editado la Reserva correctamente.')
            return redirect('reserva_lista')

    return render(request, 'reservas/crud/actualizar_reserva.html', {'formulario': formulario, 'reserva': reserva})

def reserva_eliminar(request, id_reserva):
    reserva = Reserva.objects.get(id=id_reserva)
    try:
        reserva.delete()
        messages.success(request, "Reserva eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar la reserva: {e}")
    return redirect('reserva_lista')

def reserva_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = ReservaBuscarAvanzada(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Filtros Aplicados:\n'
            qs = Reserva.objects.select_related('huesped', 'habitacion')
            
            huesped_nombre = formulario.cleaned_data.get('huesped_nombre')
            fecha_entrada_desde = formulario.cleaned_data.get('fecha_entrada_desde')
            estado = formulario.cleaned_data.get('estado')
            
            if huesped_nombre:
                qs = qs.filter(huesped__nombre__icontains=huesped_nombre)
                mensaje_busqueda += f'· Huésped contiene "{huesped_nombre}"\n'
            
            if fecha_entrada_desde:
                qs = qs.filter(fecha_entrada__gte=fecha_entrada_desde)
                mensaje_busqueda += f'· Entrada desde {fecha_entrada_desde}\n'
            
            if estado:
                qs = qs.filter(estado=estado)
                mensaje_busqueda += f'· Estado: {estado}\n'
            
            reservas = qs.all()
            return render(request, 'reservas/reserva_lista.html', {
                'reserva_lista': reservas,
                'Mensaje_Busqueda': mensaje_busqueda
            })
    else:
        formulario = ReservaBuscarAvanzada(None)
        
    return render(request, 'reservas/crud/buscar_avanzada_reserva.html', {'formulario': formulario})


# ==============================================================================
#  FACTURA CRUD
# ==============================================================================

def factura_lista(request):
    facturas = Factura.objects.select_related('reserva').all()
    return render(request, 'facturas/factura_lista.html', {'factura_lista': facturas})

def hotel_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = HotelForm(datosFormulario)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, f'Se ha creado el Hotel: [{formulario.cleaned_data.get("nombre")}] correctamente.')
            return redirect('hotel_lista')
            
    return render(request, 'hoteles/crud/create_hotel.html', {'formulario': formulario})

def hotel_editar(request, id_hotel):
    hotel = Hotel.objects.get(id=id_hotel)
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = HotelForm(datosFormulario, instance=hotel)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, f'Se ha editado el Hotel: [{formulario.cleaned_data.get("nombre")}] correctamente.')
            return redirect('hotel_lista')

    return render(request, 'hoteles/crud/actualizar_hotel.html', {'formulario': formulario, 'hotel': hotel})

def hotel_eliminar(request, id_hotel):
    hotel = Hotel.objects.get(id=id_hotel)
    try:
        hotel.delete()
        messages.success(request, "Hotel eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el hotel: {e}")
    return redirect('hotel_lista')

def hotel_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = HotelBuscarAvanzada(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Filtros Aplicados:\n'
            qs = Hotel.objects.prefetch_related('servicios')
            
            nombre_contiene = formulario.cleaned_data.get('nombre_contiene')
            calificacion_minima = formulario.cleaned_data.get('calificacion_minima')
            tiene_restaurante = formulario.cleaned_data.get('tiene_restaurante')
            
            if nombre_contiene:
                qs = qs.filter(nombre__icontains=nombre_contiene)
                mensaje_busqueda += f'· Nombre contiene "{nombre_contiene}"\n'
            
            if calificacion_minima is not None:
                qs = qs.filter(calificacion__gte=calificacion_minima)
                mensaje_busqueda += f'· Calificación >= {calificacion_minima}\n'
            
            if tiene_restaurante is not None:
                qs = qs.filter(tiene_restaurante=tiene_restaurante)
                mensaje_busqueda += f'· Restaurante: {"Sí" if tiene_restaurante else "No"}\n'
            
            hoteles = qs.all()
            return render(request, 'hoteles/hotel_lista.html', {
                'hotel_lista': hoteles,
                'Mensaje_Busqueda': mensaje_busqueda
            })
    else:
        formulario = HotelBuscarAvanzada(None)
        
    return render(request, 'hoteles/crud/buscar_avanzada_hotel.html', {'formulario': formulario})

def factura_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = FacturaForm(datosFormulario)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, f'Se ha creado la Factura: [{formulario.cleaned_data.get("numero_factura")}] correctamente.')
            return redirect('factura_lista')
            
    return render(request, 'facturas/crud/create_factura.html', {'formulario': formulario})

def factura_editar(request, id_factura):
    factura = Factura.objects.get(id=id_factura)
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = FacturaForm(datosFormulario, instance=factura)
    
    if request.method == "POST":
        if crear_modelo_generico(formulario):
            messages.success(request, f'Se ha editado la Factura: [{formulario.cleaned_data.get("numero_factura")}] correctamente.')
            return redirect('factura_lista')

    return render(request, 'facturas/crud/actualizar_factura.html', {'formulario': formulario, 'factura': factura})

def factura_eliminar(request, id_factura):
    factura = Factura.objects.get(id=id_factura)
    try:
        factura.delete()
        messages.success(request, "Factura eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar la factura: {e}")
    return redirect('factura_lista')

def factura_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = FacturaBuscarAvanzada(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Filtros Aplicados:\n'
            qs = Factura.objects.select_related('reserva')
            
            numero_contiene = formulario.cleaned_data.get('numero_contiene')
            monto_minimo = formulario.cleaned_data.get('monto_minimo')
            pagada = formulario.cleaned_data.get('pagada')
            
            if numero_contiene:
                qs = qs.filter(numero_factura__icontains=numero_contiene)
                mensaje_busqueda += f'· Número contiene "{numero_contiene}"\n'
            
            if monto_minimo is not None:
                qs = qs.filter(monto_total__gte=monto_minimo)
                mensaje_busqueda += f'· Monto >= {monto_minimo}\n'
            
            if pagada is not None:
                qs = qs.filter(pagada=pagada)
                mensaje_busqueda += f'· Pagada: {"Sí" if pagada else "No"}\n'
            
            facturas = qs.all()
            return render(request, 'facturas/factura_lista.html', {
                'factura_lista': facturas,
                'Mensaje_Busqueda': mensaje_busqueda
            })
    else:
        formulario = FacturaBuscarAvanzada(None)
        
    return render(request, 'facturas/crud/buscar_avanzada_factura.html', {'formulario': formulario})


# ==============================================================================
#  GESTIÓN DE IMÁGENES DE HOTELES
# ==============================================================================

def gestion_imagenes(request):
    """
    Vista para gestionar imágenes de hoteles.
    Permite subir nuevas imágenes y visualizar las existentes.
    """
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        formulario = HotelImageForm(datosFormulario, request.FILES)
        
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Imagen subida correctamente.')
                return redirect('gestion_imagenes')
            except Exception as e:
                messages.error(request, f'Error al subir la imagen: {e}')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        formulario = HotelImageForm()
    
    # Obtener todas las imágenes con información del hotel
    imagenes = HotelImage.objects.select_related('hotel').all()
    
    return render(request, 'hoteles/gestion_imagenes.html', {
        'formulario': formulario,
        'imagenes': imagenes
    })

