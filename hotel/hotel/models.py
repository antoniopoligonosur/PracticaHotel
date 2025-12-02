from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
import uuid




class Huesped(models.Model):
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"



class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    es_opcional = models.BooleanField(default=True)
    duracion_minutos = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

