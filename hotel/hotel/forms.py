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