# Practica Hotel

Este proyecto es una aplicación web desarrollada con Django para la gestión integral de hoteles. Permite administrar hoteles, habitaciones, huéspedes, reservas, servicios adicionales y facturación de manera sencilla y eficiente.

-----------------------------------

# DIAGRAMA ENTIDAD RELACION:

-----------------------------------

# EXPLICACION DE MODELOS Y ATRIBUTOS USADOS:

# Hotel: información general del hotel.
- nombre: nombre único del hotel.
- descripcion: breve descripción.
- direccion: ubicación del hotel.
- fecha_fundacion: fecha en que se fundó.
- calificacion: valoración media (ej. 4.5 estrellas).
- servicios: relación M2M con los servicios que ofrece el hotel.

# ContactoHotel: datos de contacto del hotel.
- hotel: relación uno a uno con Hotel.
- nombre_contacto: persona encargada.
- telefono: número de teléfono validado.
- correo: email de contacto único.
- sitio_web: página web opcional.

# TipoHabitacion: define las características de cada tipo de habitación.
- nombre: tipo (simple, doble, suite...).
- descripcion: información adicional.
- capacidad: número máximo de huéspedes.
- precio_base: precio base por noche.

# Habitacion: representa una habitación física en el hotel.
- numero: número identificador.
- piso: planta donde se encuentra.
- tipo: tipo de habitación (ForeignKey a TipoHabitacion).
- hotel: hotel al que pertenece.
- disponible: indica si está libre.
- imagen_url: enlace a una foto.
- servicios: servicios disponibles en la habitación.

# Huesped: información básica del cliente.
- nombre y apellido: datos personales.
- correo: email único.
- telefono: contacto opcional.
- fecha_nacimiento: fecha opcional.

# PerfilHuesped: información complementaria del huésped.
- huesped: relación uno a uno con Huesped.
- nacionalidad: país de origen.
- numero_pasaporte: documento único opcional.
- puntos_fidelidad: puntos acumulados.
- preferencias: gustos o solicitudes especiales.

# Servicio: servicios ofrecidos por el hotel.
- nombre: nombre del servicio (ej. Spa, desayuno...).
- descripcion: detalles opcionales.
- precio: coste del servicio.
- es_opcional: indica si el servicio es extra.
- duracion_minutos: duración (ej. 60 min en spa).

# Reserva: registro de una estancia.
- huesped: cliente que reserva.
- habitacion: habitación reservada.
- fecha_entrada / fecha_salida: rango de fechas.
- estado: estado de la reserva (Pendiente, Confirmada, etc.).
- creada_en: fecha y hora de creación.
- servicios: relación M2M con Servicio (a través de ReservaServicio).

# Factura: documento generado por una reserva.
- reserva: relación uno a uno con la reserva.
- emitida_en: fecha de emisión.
- numero_factura: identificador único (UUID).
- monto_total: total a pagar.
- pagada: si ya está pagada.
- notas: observaciones opcionales.

# ReservaServicio: tabla intermedia entre Reserva y Servicio.
- reserva / servicio: relaciones principales.
- cantidad: número de unidades del servicio.
- precio_en_momento: precio en el momento de la reserva.
- nota: texto opcional.

-----------------------------------

# PARAMETROS USADOS EN "models":

max_length → define el número máximo de caracteres permitidos en campos tipo texto (CharField, EmailField...).  
unique → evita que se repitan valores en la base de datos (crea una restricción de unicidad).  
null → permite que el campo quede vacío en la base de datos.  
blank → permite dejar el campo vacío en los formularios o panel de administración.  
default → asigna un valor por defecto si no se proporciona ninguno.  
validators → lista de validaciones personalizadas, como MinValueValidator o RegexValidator.  
choices → limita el valor del campo a una lista de opciones predefinidas (ej. estados de reserva).  
related_name → nombre alternativo para acceder a la relación inversa desde el modelo relacionado.  
on_delete → define qué ocurre cuando se elimina el objeto relacionado (CASCADE, PROTECT, etc.).  
auto_now_add → guarda automáticamente la fecha/hora al crear el registro.  
max_digits → número total de dígitos en un campo DecimalField.  
decimal_places → cantidad de dígitos después del punto decimal.  
through → especifica un modelo intermedio personalizado para una relación ManyToMany.  
validators=[MinValueValidator(1)] → asegura que un número sea al menos 1.  
RegexValidator(r'^\+?\d{7,15}$') → valida que el número de teléfono tenga entre 7 y 15 dígitos y pueda incluir “+”.  
UUIDField(default=uuid.uuid4) → genera identificadores únicos automáticos para cada registro.  
BooleanField(default=True/False) → campo de tipo verdadero/falso con valor por defecto.  
URLField → campo para almacenar enlaces válidos.  
EmailField → campo específico para correos electrónicos.  
DateField → almacena una fecha (año, mes, día).  
DateTimeField → almacena fecha y hora.  
TextField → campo para textos largos sin límite de caracteres.  
IntegerField → almacena números enteros (sin decimales).  
DecimalField → almacena números con decimales, controlando la precisión.  
ManyToManyField → relación de muchos a muchos entre modelos.  
ForeignKey → relación de muchos a uno (varios registros pueden referir al mismo objeto).  
OneToOneField → relación de uno a uno entre dos modelos.

-----------------------------------

# EXPLICACION DE PARAMETROS USADOS EN "generar_datos"

from django.db import transaction → Sirve para agrupar varias operaciones en una sola "transacción".  
Si algo falla dentro de transaction.atomic(), se deshace todo (rollback).  
from faker import Faker → Faker('es_ES') para datos en español.  
import random → elegir aleatorios (choice, sample, randint).  
import uuid → generar identificadores únicos (por ejemplo numero_factura).  
from datetime import timedelta → operaciones con fechas (salida = entrada + días).  
from decimal import Decimal → precisión correcta en importes monetarios.

# Semillas:
Faker.seed(0); random.seed(0) → reproducibilidad: mismas entradas aleatorias en cada ejecución.

# Uso de fake.unique:
fake.unique.xxx() → evita duplicados en campos con unique=True (emails, nombres de empresa, etc).

# transaction.atomic():
Agrupar la creación en una transacción para que, si hay error, se haga rollback completo.

# Decimal y formateo de precios:
Usar Decimal(f"{random.uniform(5,150):.2f}") para crear precios con 2 decimales.  
Usar .quantize(Decimal('0.01')) al sumar totales para forzar 2 decimales.

# Fechas y duración:
fecha_entrada = fake.date_between(...); fecha_salida = fecha_entrada + timedelta(days=dias)  
→ garantiza fecha_salida posterior y evita violar validaciones lógicas.

# Faker helpers útiles:
fake.image_url(), fake.company(), fake.company_email(), fake.phone_number(), fake.date_of_birth(...)  
bothify: fake.bothify('??######') → generar pasaportes o códigos con letras y números

-----------------------------------
