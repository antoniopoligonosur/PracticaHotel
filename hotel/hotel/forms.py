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