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


class ContactoHotel(models.Model):
    nombre_contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, validators=[RegexValidator(r'^\+?\d{7,15}$')])
    correo = models.EmailField(unique=True)
    sitio_web = models.URLField(null=True, blank=True)
    
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='contacto')

    def __str__(self):
        return self.nombre_contacto


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

class PerfilHuesped(models.Model):
    huesped = models.OneToOneField(Huesped, on_delete=models.CASCADE, related_name='perfil')
    nacionalidad = models.CharField(max_length=50)
    numero_pasaporte = models.CharField(max_length=30, null=True, blank=True, unique=True)
    puntos_fidelidad = models.IntegerField(default=0)
    preferencias = models.TextField(blank=True)

    def __str__(self):
        return self.huesped.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    es_opcional = models.BooleanField(default=True)
    duracion_minutos = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    ESTADOS = [
        ('P', 'Pendiente'),
        ('C', 'Confirmada'),
        ('F', 'Finalizada'),
        ('X', 'Cancelada'),
    ]
    huesped = models.ForeignKey(Huesped, on_delete=models.CASCADE, related_name='reservas')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT, related_name='reservas')
    servicios = models.ManyToManyField(Servicio, through='ReservaServicio', blank=True, related_name='reservas')
    
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    creada_en = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Reserva {self.id} - {self.huesped.nombre}"


class Factura(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='factura')
    emitida_en = models.DateTimeField(auto_now_add=True)
    numero_factura = models.CharField(max_length=30, unique=True, default=uuid.uuid4)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    pagada = models.BooleanField(default=False)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Factura {self.numero_factura}"


class ReservaServicio(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    precio_en_momento = models.DecimalField(max_digits=8, decimal_places=2)
    nota = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.servicio.nombre} (Reserva {self.reserva.id})"
