import datetime
from django.forms import ModelForm
from .models import *

# Ahora vamos a definir nuestro formulario para el modelo Huespued (Model Forms)

class Huesped(ModelForm):
    class Meta:

        model = Huesped
        fields = ["nombre", "apellido", "correo", "telefono", "fecha_nacimiento"]
        labels = {
            "nombre": ("Nombre Huesped"),
            "apellido": ("Apellido Huesped"),
            "correo": ("Correo Huesped"),
            "telefono": ("Telefono Huesped"),
            "fecha_nacimiento": ("Fecha Nacimiento Huesped"),
        }
        help_texts = {
            "nombre": ("30 caracteres como minimo")
        }

