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
            "fecha_nacimiento":forms.DateInput(attrs={'type':'date'})
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
