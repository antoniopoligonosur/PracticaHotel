from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
import uuid


class Hotel(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=200)
    fecha_fundacion = models.DateField(null=True, blank=True)
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    num_habitaciones = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    tiene_restaurante = models.BooleanField(default=False)
    correo_contacto = models.EmailField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)                   
    hora_apertura = models.TimeField(null=True, blank=True)
    
    servicios = models.ManyToManyField('Servicio', blank=True, related_name='hoteles')

    def __str__(self):
        return self.nombre




class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    capacidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_base = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    numero = models.CharField(max_length=10)
    piso = models.IntegerField()
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.PROTECT, related_name='habitaciones')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='habitaciones')
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='habitaciones/', null=True, blank=True)
    servicios = models.ManyToManyField('Servicio', blank=True, related_name='habitaciones')

    def __str__(self):
        return f"{self.hotel.nombre} - Habitación {self.numero}"


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

