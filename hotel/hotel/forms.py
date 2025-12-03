from django import forms
from django.forms import ModelForm
from .models import *
import datetime

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

class HabitacionImageForm(ModelForm):
    class Meta:
        model = Habitacion
        fields = ['imagen']
        labels = {
            "imagen": ("Imagen de la Habitación"),
        }

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
        if nombre_contacto and len(nombre_contacto) < 3:
            self.add_error('nombre_contacto', 'El nombre debe tener al menos 3 caracteres.')
        
        telefono = self.cleaned_data.get('telefono')
        if telefono and len(telefono) < 9:
            self.add_error('telefono', 'El teléfono debe tener al menos 9 dígitos.')
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
    telefono_contiene = forms.CharField(
        label='Teléfono contiene',
        required=False,
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        nombre_contacto_contiene = self.cleaned_data.get('nombre_contacto_contiene')
        correo_contiene = self.cleaned_data.get('correo_contiene')
        telefono_contiene = self.cleaned_data.get('telefono_contiene')

        if not any([nombre_contacto_contiene, correo_contiene, telefono_contiene]):
            self.add_error('nombre_contacto_contiene', 'Debe rellenar al menos un campo.')
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
        if nacionalidad and len(nacionalidad) < 3:
            self.add_error('nacionalidad', 'La nacionalidad debe tener al menos 3 caracteres.')
            
        puntos = self.cleaned_data.get('puntos_fidelidad')
        if puntos is not None and puntos < 0:
            self.add_error('puntos_fidelidad', 'Los puntos no pueden ser negativos.')
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
    numero_pasaporte_contiene = forms.CharField(
        label='Número pasaporte contiene',
        required=False,
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        nacionalidad_contiene = self.cleaned_data.get('nacionalidad_contiene')
        puntos_minimos = self.cleaned_data.get('puntos_minimos')
        numero_pasaporte_contiene = self.cleaned_data.get('numero_pasaporte_contiene')

        if not any([nacionalidad_contiene, puntos_minimos is not None, numero_pasaporte_contiene]):
            self.add_error('nacionalidad_contiene', 'Debe rellenar al menos un campo.')
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