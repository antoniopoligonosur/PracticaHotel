from django import forms
from django.forms import ModelForm
from .models import *

# Ahora vamos a definir nuestro formulario para el modelo Huespued (Model Forms)

class HuespedForm(ModelForm):
    class Meta:

        model = Huesped
        fields = "__all__"
        labels = {
            "nombre": ("Nombre Huesped"),
            "apellido": ("Apellido Huesped"),
            "correo": ("Correo Huesped"),
            "telefono": ("Telefono Huesped"),
            "fecha_nacimiento": ("Fecha Nacimiento Huesped"),
        }
        help_texts = {
            "nombre": ("80 caracteres como maximo"),
            "apellido": ("80 caracteres como maximo")
        }
        widgets = {
            "fecha_nacimiento":forms.DateInput(attrs={'type':'date'}, format='%Y-%m-%d')
        }
        localized_fields = ["fecha_nacimiento"]
        
    def clean(self):

        #Validaciones basicas de todos mis modelos usando clean 
        super().clean()

        #Obtenemos los campos para hacer validaciones personalizadas
        nombre = self.cleaned_data.get('nombre')
        telefono = self.cleaned_data.get('telefono')

        #Personalizamos validaciones
        if len(nombre) < 3:
            self.add_error('nombre','El nombre debe tener al menos 3 caracteres.')

        if len(telefono) < 9:
            self.add_error('telefono','El telefono debe de tener 9 numeros.')

        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# -----------------------------------------------------------------------------
# HOTEL
# -----------------------------------------------------------------------------
class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = "__all__"
        labels = {
            "nombre": ("Nombre del Hotel"),
            "descripcion": ("Descripción"),
            "direccion": ("Dirección"),
            "fecha_fundacion": ("Fecha de Fundación"),
            "calificacion": ("Calificación"),
            "num_habitaciones": ("Número de Habitaciones"),
            "tiene_restaurante": ("¿Tiene Restaurante?"),
            "correo_contacto": ("Correo de Contacto"),
            "sitio_web": ("Sitio Web"),
            "hora_apertura": ("Hora de Apertura"),
            "servicios": ("Servicios"),
        }
        widgets = {
            "fecha_fundacion": forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            "hora_apertura": forms.TimeInput(attrs={'type': 'time'}),
            "descripcion": forms.Textarea(attrs={'rows': 3}),
        }
        localized_fields = ["fecha_fundacion"]

    def clean(self):
        super().clean()
        num_habitaciones = self.cleaned_data.get('num_habitaciones')
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) < 3:
            self.add_error('nombre', 'El nombre debe tener al menos 3 caracteres.')
        if num_habitaciones and num_habitaciones > 100:
            self.add_error('num_habitaciones', 'Los hoteles no pueden tener más de 100 habitaciones.')
        return self.cleaned_data

class HotelBuscarAvanzada(forms.Form):
    nombre_contiene = forms.CharField(
        label='Nombre contiene',
        required=False,
        help_text="(Opcional)"
    )
    calificacion_minima = forms.DecimalField(
        label='Calificación mínima',
        required=False,
        decimal_places=2,
        help_text="(Opcional)"
    )
    tiene_restaurante = forms.NullBooleanField(
        label='¿Tiene restaurante?',
        required=False,
        widget=forms.Select(choices=[
            (None, 'Indiferente'),
            (True, 'Sí'),
            (False, 'No')
        ]),
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        nombre_contiene = self.cleaned_data.get('nombre_contiene')
        calificacion_minima = self.cleaned_data.get('calificacion_minima')
        tiene_restaurante = self.cleaned_data.get('tiene_restaurante')

        if not any([nombre_contiene, calificacion_minima, tiene_restaurante is not None]):
            self.add_error('nombre_contiene', 'Debe rellenar al menos un campo.')
        if(
            calificacion_minima and calificacion_minima < 0
            ):
            self.add_error('calificacion_minima','La calificacion debe ser mayor que cero.')
        
        return self.cleaned_data

# -----------------------------------------------------------------------------
# CONTACTO HOTEL
# -----------------------------------------------------------------------------
class ContactoHotelForm(ModelForm):
    class Meta:
        model = ContactoHotel
        fields = "__all__"
        labels = {
            "nombre_contacto": ("Nombre del Contacto"),
            "telefono": ("Teléfono"),
            "correo": ("Correo Electrónico"),
            "sitio_web": ("Sitio Web"),
            "hotel": ("Hotel Asociado"),
        }
    
    def clean(self):
        super().clean()
        nombre_contacto = self.cleaned_data.get('nombre_contacto')
        sitio_web = self.cleaned_data.get('sitio_web')
        if nombre_contacto and len(nombre_contacto) < 5:
            self.add_error('nombre_contacto', 'El nombre debe tener al menos 5 caracteres.')
        if sitio_web and len(sitio_web) < 10:
            self.add_error('nombre_contacto', 'La URL debe tener al menos 10 caracteres.')
        return self.cleaned_data

class ContactoHotelBuscarAvanzada(forms.Form):
    nombre_contacto_contiene = forms.CharField(
        label='Nombre contacto contiene',
        required=False,
        help_text="(Opcional)"
    )
    correo_contiene = forms.CharField(
        label='Correo contiene',
        required=False,
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        nombre_contacto_contiene = self.cleaned_data.get('nombre_contacto_contiene')
        correo_contiene = self.cleaned_data.get('correo_contiene')
        # Funcionamiento del "if not any": si ninguno de los dos campos tiene datos, se lanza el error.
        if not any([nombre_contacto_contiene, correo_contiene]):
            self.add_error('nombre_contacto_contiene', 'Debe rellenar al menos un campo.')
        if(
            correo_contiene and len(correo_contiene) < 3
            ):
            self.add_error('calificacion_minima','La calificacion debe ser mayor que cero.')
        return self.cleaned_data


# -----------------------------------------------------------------------------
# PERFIL HUESPED
# -----------------------------------------------------------------------------
class PerfilHuespedForm(ModelForm):
    class Meta:
        model = PerfilHuesped
        fields = "__all__"
        labels = {
            "huesped": ("Huésped"),
            "nacionalidad": ("Nacionalidad"),
            "numero_pasaporte": ("Número de Pasaporte"),
            "puntos_fidelidad": ("Puntos de Fidelidad"),
            "preferencias": ("Preferencias"),
        }
        widgets = {
            "preferencias": forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        super().clean()
        nacionalidad = self.cleaned_data.get('nacionalidad')
        preferencias = self.cleaned_data.get('preferencias')
        if nacionalidad and len(nacionalidad) < 3:
            self.add_error('nacionalidad', 'La nacionalidad debe tener al menos 3 caracteres.')
        if preferencias and len(preferencias) < 10:
            self.add_error('preferencias', 'Las preferencias deben tener al menos 10 caracteres.')
        return self.cleaned_data

class PerfilHuespedBuscarAvanzada(forms.Form):
    nacionalidad_contiene = forms.CharField(
        label='Nacionalidad contiene',
        required=False,
        help_text="(Opcional)"
    )
    puntos_minimos = forms.IntegerField(
        label='Puntos mínimos',
        required=False,
        min_value=0,
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        nacionalidad_contiene = self.cleaned_data.get('nacionalidad_contiene')
        puntos_minimos = self.cleaned_data.get('puntos_minimos')

        if not any([nacionalidad_contiene, puntos_minimos is not None]):
            self.add_error('nacionalidad_contiene', 'Debe rellenar al menos un campo.')
        if(
            puntos_minimos and puntos_minimos < 0
            ):
            self.add_error('puntos_minimos','Los puntos minimos deben ser mayor que cero.')
        return self.cleaned_data


# -----------------------------------------------------------------------------
# RESERVA
# -----------------------------------------------------------------------------
class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = "__all__"
        # Excluimos 'creada_en' porque es auto_now_add y no editable
        exclude = ['creada_en']
        labels = {
            "huesped": ("Huésped"),
            "habitacion": ("Habitación"),
            "fecha_entrada": ("Fecha de Entrada"),
            "fecha_salida": ("Fecha de Salida"),
            "estado": ("Estado"),
        }
        widgets = {
            "fecha_entrada": forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            "fecha_salida": forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        localized_fields = ["fecha_entrada", "fecha_salida"]

    def clean(self):
        super().clean()
        fecha_entrada = self.cleaned_data.get('fecha_entrada')
        fecha_salida = self.cleaned_data.get('fecha_salida')

        if fecha_entrada and fecha_salida and fecha_salida < fecha_entrada:
            self.add_error('fecha_salida', 'La fecha de salida no puede ser anterior a la de entrada.')
        return self.cleaned_data

class ReservaBuscarAvanzada(forms.Form):
    huesped_nombre = forms.CharField(
        label='Nombre Huésped contiene',
        required=False,
        help_text="(Opcional)"
    )
    fecha_entrada_desde = forms.DateField(
        label='Fecha entrada desde',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="(Opcional)"
    )
    estado = forms.ChoiceField(
        label='Estado',
        choices=[('', 'Cualquiera')] + Reserva.ESTADOS,
        required=False,
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        huesped_nombre = self.cleaned_data.get('huesped_nombre')
        fecha_entrada_desde = self.cleaned_data.get('fecha_entrada_desde')
        estado = self.cleaned_data.get('estado')

        if not any([huesped_nombre, fecha_entrada_desde, estado]):
            self.add_error('huesped_nombre', 'Debe rellenar al menos un campo.')
        return self.cleaned_data

# -----------------------------------------------------------------------------
# FACTURA
# -----------------------------------------------------------------------------
class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        fields = "__all__"
        # 'emitida_en' es auto_now_add
        exclude = ['emitida_en'] 
        labels = {
            "reserva": ("Reserva"),
            "numero_factura": ("Número de Factura"),
            "monto_total": ("Monto Total"),
            "pagada": ("¿Pagada?"),
            "notas": ("Notas"),
        }
        widgets = {
            "notas": forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        super().clean()
        monto_total = self.cleaned_data.get('monto_total')
        if monto_total and monto_total < 0:
            self.add_error('monto_total', 'El monto no puede ser negativo.')
        return self.cleaned_data

class FacturaBuscarAvanzada(forms.Form):
    numero_contiene = forms.CharField(
        label='Número factura contiene',
        required=False,
        help_text="(Opcional)"
    )
    monto_minimo = forms.DecimalField(
        label='Monto mínimo',
        required=False,
        decimal_places=2,
        help_text="(Opcional)"
    )
    pagada = forms.NullBooleanField(
        label='¿Pagada?',
        required=False,
        widget=forms.Select(choices=[
            (None, 'Indiferente'),
            (True, 'Sí'),
            (False, 'No')
        ]),
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        numero_contiene = self.cleaned_data.get('numero_contiene')
        monto_minimo = self.cleaned_data.get('monto_minimo')
        pagada = self.cleaned_data.get('pagada')

        if not any([numero_contiene, monto_minimo is not None, pagada is not None]):
            self.add_error('numero_contiene', 'Debe rellenar al menos un campo.')
        return self.cleaned_data

class HuespedBuscarAvanzada(forms.Form):

    nombre_huesped_contiene = forms.CharField(
        label='Nombre de huesped contiene',
        help_text="(Opcional)",
        required=False
    )

    fecha_nacimiento_desde = forms.DateField(
        label='nacimiento desde',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateInput(attrs={'type':'date'})
    )

    fecha_nacimiento_hasta = forms.DateField(
        label='nacimiento hasta',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateInput(attrs={'type':'date'})
    )

    def clean(self):

        #Validamos con el modelo actual
        super().clean()

        #Obtenemos los campos
        nombre_huesped_contiene = self.cleaned_data.get('nombre_huesped_contiene')
        fecha_nacimiento_desde = self.cleaned_data.get('fecha_nacimiento_desde')
        fecha_nacimiento_hasta = self.cleaned_data.get('fecha_nacimiento_hasta')
        
        #Comprobamos
        if(
            nombre_huesped_contiene == "" and
            fecha_nacimiento_desde is None and
            fecha_nacimiento_hasta is None
        ):
            self.add_error('nombre_huesped_contiene','Debe de rellenar al menos un campo.')
            self.add_error('fecha_nacimiento_desde','Debe de rellenar al menos un campo.')
            self.add_error('fecha_nacimiento_hasta','Debe de rellenar al menos un campo.')
        
        if(
            not fecha_nacimiento_desde is None and
            not fecha_nacimiento_hasta is None and
            fecha_nacimiento_hasta < fecha_nacimiento_desde
            ):
            self.add_error('fecha_nacimiento_desde','Rango de fecha no valido.')
            self.add_error('fecha_nacimiento_hasta','Rango de fecha no valido.')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
