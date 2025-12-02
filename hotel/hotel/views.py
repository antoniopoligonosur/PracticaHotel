from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum, Avg, Min, Max, Prefetch
from django.views.defaults import page_not_found
from django.db.models import Q
from .models import (
    Huesped, Servicio
)
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect

def index(request):
    return render(request, 'base/index.html')

def huesped_lista(request):
    huesped = Huesped.objects.all()
    
    return render(request, 'huespedes/huesped_lista.html', {'huesped_lista':huesped})



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










