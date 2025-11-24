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
            "nombre": ("30 caracteres como maximo"),
            "apellido": ("60 caracteres como maximo")
        }
        widgets = {
            "fecha_nacimiento":forms.SelectDateWidget()
        }
        localized_fields = ["fecha_nacimiento"]
