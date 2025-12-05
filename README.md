# Practica Hotel

Este proyecto es una aplicación web desarrollada con Django para la gestión integral de hoteles. Permite administrar hoteles, habitaciones, huéspedes, reservas, servicios adicionales y facturación de manera sencilla y eficiente.

-----------------------------------

# DIAGRAMA ENTIDAD RELACION:

<img width="1696" height="1093" alt="Diagrama_Antonio_Mateos_Delgado drawio" src="https://github.com/user-attachments/assets/c06bda56-89e7-4a62-9bf1-f647bb898fa4" />

-----------------------------------

# EXPLICACION DE MODELOS Y ATRIBUTOS USADOS:

# Hotel: información general del hotel.
- nombre: nombre único del hotel.
- descripcion: breve descripción.
- direccion: ubicación del hotel.
- fecha_fundacion: fecha en que se fundó.
- calificacion: valoración media (ej. 4.5 estrellas).
- num_habitaciones: número total de habitaciones, validado con **MinValueValidator(1)** para evitar valores menores a 1.
- tiene_restaurante: indica si el hotel cuenta con restaurante.
- correo_contacto: correo de contacto opcional.
- sitio_web: página web del hotel.
- hora_apertura: hora en la que abre el hotel.
- servicios: relación ManyToMany con los servicios que ofrece el hotel.

# ContactoHotel: datos de contacto del hotel.
- hotel: relación uno a uno con Hotel.
- nombre_contacto: persona encargada.
- telefono: número de teléfono validado mediante **RegexValidator(r'^\+?\d{7,15}$')**.
- correo: email de contacto único.
- sitio_web: página web opcional.

# TipoHabitacion: define las características de cada tipo de habitación.
- nombre: tipo (simple, doble, suite...).
- descripcion: información adicional.
- capacidad: número máximo de huéspedes, validado con **MinValueValidator(1)**.
- precio_base: precio base por noche.

# Habitacion: representa una habitación física en el hotel.
- numero: número identificador.
- piso: planta donde se encuentra.
- tipo: tipo de habitación (ForeignKey a TipoHabitacion).
- hotel: hotel al que pertenece.
- disponible: indica si está libre.
- imagen_url: enlace a una foto.
- servicios: servicios disponibles en la habitación (ManyToMany con Servicio).

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
- estado: estado de la reserva (Pendiente, Confirmada, Finalizada, Cancelada).
- creada_en: fecha y hora de creación.
- servicios: relación ManyToMany con Servicio a través del modelo intermedio ReservaServicio.

# Factura: documento generado por una reserva.
- reserva: relación uno a uno con la reserva.
- emitida_en: fecha de emisión.
- numero_factura: identificador único generado automáticamente con **uuid.uuid4**.
- monto_total: total a pagar.
- pagada: indica si la factura está pagada.
- notas: observaciones opcionales.

# ReservaServicio: tabla intermedia entre Reserva y Servicio.
- reserva / servicio: relaciones principales.
- cantidad: número de unidades del servicio, validado con **MinValueValidator(1)**.
- precio_en_momento: precio del servicio en el momento de la reserva.
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
**MinValueValidator(1)** → asegura que un número sea al menos 1 (por ejemplo, capacidad, cantidad o número de habitaciones).  
**RegexValidator(r'^\+?\d{7,15}$')** → valida que el número de teléfono tenga entre 7 y 15 dígitos y pueda incluir “+”.  
**uuid.uuid4** → genera identificadores únicos automáticos para cada registro.  
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
bothify: fake.bothify('??######') → generar pasaportes o códigos con letras y números.

-----------------------------------

# URLs Y VISTAS IMPLEMENTADAS

Este proyecto cuenta con 10 URLs principales, cada una asociada a una vista que realiza operaciones sobre los modelos y relaciones entre ellos. 

La primera URL, `/contacto/lista`, está vinculada a la vista `contacto_lista`. Esta vista muestra todos los contactos de los hoteles, incluyendo la información relacionada del hotel al que pertenecen. Se utiliza una relación ManyToOne entre `ContactoHotel` y `Hotel` y el QuerySet está optimizado mediante `select_related`. Además, se incluye un ejemplo comentado de cómo sería la misma consulta en SQL crudo.

La segunda URL, `/hotel/lista`, corresponde a la vista `hotel_lista`. Esta vista lista los hoteles junto con sus servicios, estableciendo la relación ManyToMany entre `Hotel` y `Servicio`. Para optimizar la consulta y evitar el problema N+1, se utiliza `prefetch_related`. Además, se limita la lista a los 10 hoteles con mejor calificación.

La tercera URL, `/tipohabitacion/lista`, acepta un parámetro GET opcional `nombre` y se maneja con la vista `tipo_habitacion_lista`. Esta vista permite filtrar los tipos de habitación que contengan un determinado texto en el nombre. En el QuerySet se puede observar un filtro OR comentado en SQL para mostrar cómo se podrían combinar varias condiciones.

La cuarta URL, `/habitacion/lista/<int:hotel_id>/`, está asociada a la vista `habitacion_lista`. Esta vista muestra todas las habitaciones de un hotel específico, incluyendo su tipo, los servicios asociados y la información del hotel. Se utilizan relaciones ManyToOne (`Habitacion → Hotel`) y ManyToMany (`Habitacion ↔ Servicio`), y se optimiza la consulta usando `select_related` y `prefetch_related`.

La quinta URL, `/detalles_hotel/<int:id_hotel>/`, conecta con la vista `detalle_hotel`. Permite obtener la información completa de un hotel específico junto con todos sus servicios. Se utiliza `prefetch_related` para optimizar la carga de las relaciones ManyToMany.

La sexta URL, `/perfil_huesped/lista`, está ligada a la vista `perfil_huesped_lista`. Esta vista muestra los perfiles de los huéspedes junto con la información básica de cada huésped, utilizando la relación OneToOne entre `PerfilHuesped` y `Huesped`. La consulta está optimizada con `select_related`.

La séptima URL, `/servicio/lista`, corresponde a la vista `servicio_lista`. Esta vista muestra todos los servicios disponibles en el hotel y ejemplifica el uso de filtros OR y ordenamientos, además de mostrar cómo se podrían aplicar condiciones SQL comentadas.

La octava URL, `/hotel/lista/<int:anyo_hotel>/<int:mes_hotel>`, se gestiona mediante la vista `dame_hotel_fecha`. Permite filtrar los hoteles fundados en un año y mes concretos. La consulta utiliza `prefetch_related` y filtros combinados con AND para obtener los resultados correctos.

La novena URL utiliza `re_path` con expresión regular: `r'^hotel/calificacion/(?P<calificacion_hotel>0\.\d{2})/$'` y está asociada a la vista `dame_hotel_calificacion`. Esta vista permite filtrar hoteles por calificación exacta usando un parámetro string y demuestra cómo se pueden usar expresiones regulares para la validación en URLs.

Finalmente, la décima URL, `/hoteles/estadisticas_calificacion/`, conecta con la vista `hoteles_estadisticas_calificacion`. Esta vista calcula estadísticas sobre la calificación de los hoteles, incluyendo media, máximo y mínimo, usando funciones de agregación con `aggregate`.

# Uso de Template Tags en el Proyecto

| Archivo HTML                  | Template Tags Usados            | Descripción                                                                                                               |
|-------------------------------|--------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| `_contacto_item.html`          | `if`, `else`                   | Verifica si el teléfono existe usando `!= "-"`. Si no lo está, muestra “Sin teléfono”.                                     |
| `contacto_lista.html`          | `for`, `empty`, `include`      | Itera sobre la lista de contactos e incluye la plantilla parcial `_contacto_item.html`. Usa `empty` si no hay contactos. |
| `_factura_item.html`           | `if`, `else`                   | Evalúa si la factura está pagada y si el monto es mayor que 0.                                                            |
| `_reserva_item.html`           | `if`, `else`                   | Indica si la reserva está activa usando `or` para distintos estados.                                                     |
| `detalle_hotel.html`           | `if`, `for`, `empty`           | Recorre los servicios del hotel e indica si son gratis usando `==`.                                                      |

---

# Uso de operadores en los if

| Operador | Archivo HTML                | Ejemplo                                                                                       | Descripción                                                                |
|----------|----------------------------|------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `==`     | `detalle_hotel.html`       | `{% if servicio.precio == 0 %}`                                                              | Evalúa si el precio del servicio es 0 para mostrar “Gratis”.               |
| `!=`     | `_contacto_item.html`      | `{% if c.telefono != "-" %}`                                                                 | Verifica si el campo teléfono tiene valor distinto a “-”.                  |
| `>`      | `_hotel_item.html`         | `{% if h.calificacion|floatformat:2 > 4.5 %}`                                               | Indica “Muy bien valorado” si la calificación es mayor a 4.5.             |
| `and`    | `_factura_item.html`       | `{% if f.pagada and f.monto_total > 0 %}`                                                   | Muestra “Sí (importe válido)” solo si la factura está pagada y monto >0.  |
| `or`     | `_reserva_item.html`       | `{% if r.estado == "confirmada" or r.estado == "en_proceso" %}`                             | Considera activa la reserva si su estado es “confirmada” o “en_proceso”.  |

---

# Template Filters

| HTML                       | Template Filters Usados        | Descripción                                               |
|-----------------------------|-------------------------------|-----------------------------------------------------------|
| `_hotel_item.html`          | `title`                        | Coloca la primera letra de cada palabra del nombre en mayúscula. |
| `_hotel_item.html`          | `truncatechars`               | Trunca la descripción del hotel a 80 caracteres.        |
| `_hotel_item.html`          | `floatformat`                 | Muestra la calificación con 2 decimales.                |
| `_hotel_item.html`          | `upper`                        | Convierte el nombre del hotel a mayúsculas.             |
| `_contacto_item.html`       | `default`                      | Muestra "-" si no hay valor en los campos.              |
| `_contacto_item.html`       | `default_if_none`              | Muestra "-" si `sitio_web` es None.                     |
| `_factura_item.html`        | `floatformat`                  | Muestra el monto total con 2 decimales.                 |
| `_reserva_item.html`        | `date`                         | Formatea las fechas de entrada y salida a "d-m-Y".      |
| `detalle_hotel.html`        | `capfirst`                     | Coloca la primera letra del nombre del servicio en mayúscula. |
| `_hotel_item.html`          | `default`                       | Muestra "Sin descripción" si el hotel no tiene descripción. |

---

# VALIDACIONES IMPLEMENTADAS EN FORMULARIOS

Se han implementado validaciones personalizadas en el método `clean()` de los formularios para asegurar la integridad de los datos, cumpliendo con el requisito de tener al menos dos validaciones por formulario (además de las propias del modelo):

1. **HotelForm**:
    - **Nombre**: Se valida que el nombre tenga al menos 3 caracteres.
    - **Número de Habitaciones**: Se valida que no supere las 100 habitaciones.

2. **HuespedForm**:
    - **Nombre**: Se valida que el nombre tenga al menos 3 caracteres.
    - **Teléfono**: Se valida que el teléfono tenga 9 números.

3. **ContactoHotelForm**:
    - **Teléfono**: Se valida que el número de teléfono tenga al menos 9 dígitos.
    - **Nombre**: (Existente) Se valida que el nombre tenga al menos 3 caracteres.

4. **PerfilHuespedForm**:
    - **Puntos de Fidelidad**: Se valida que los puntos no sean negativos.
    - **Nacionalidad**: (Existente) Se valida que la nacionalidad tenga al menos 3 caracteres.

5. **ReservaForm**:
    - **Fecha de Entrada**: Se valida que la fecha de entrada no sea anterior al día actual (no se permiten reservas en el pasado).
    - **Fecha de Salida**: (Existente) Se valida que la fecha de salida sea posterior a la de entrada.

6. **FacturaForm**:
    - **Número de Factura**: Se valida que el número de factura tenga al menos 5 caracteres.
    - **Monto Total**: (Existente) Se valida que el monto total sea mayor que 0.

7. **Formularios de Búsqueda Avanzada**:
    - **Validación General**: En todos los formularios de búsqueda avanzada (`HotelBuscarAvanzada`, `ContactoHotelBuscarAvanzada`, `PerfilHuespedBuscarAvanzada`, `ReservaBuscarAvanzada`, `FacturaBuscarAvanzada`, `HuespedBuscarAvanzada`) se valida que se rellene al menos un campo.
    - **Validaciones Específicas**:
        - **Calificación/Monto/Puntos**: Se valida que sean valores positivos.
        - **Rangos de Fecha**: Se valida que la fecha 'hasta' no sea anterior a la fecha 'desde'.
        - **Longitud de Texto**: Se valida que los campos de texto no estén vacíos si se usan.
---

# WIDGETS USADOS EN FORMULARIOS

Se han utilizado 6 widgets diferentes de Django para mejorar la experiencia de usuario en los formularios:

1. **DateInput (`type='date'`)**: 
   - **Formularios**: `HotelForm` (fecha de fundación), `ReservaForm` (fechas de entrada y salida), `HuespedBuscarAvanzada` (fechas de nacimiento desde/hasta)
   - **Descripción**: Muestra un selector de fecha nativo del navegador con calendario desplegable.

2. **TimeInput (`type='time'`)**: 
   - **Formularios**: `HotelForm` (hora de apertura)
   - **Descripción**: Muestra un selector de hora nativo del navegador con formato 24 horas.

3. **Textarea (`rows=3`)**: 
   - **Formularios**: `HotelForm` (descripción), `PerfilHuespedForm` (preferencias), `FacturaForm` (notas)
   - **Descripción**: Área de texto multilínea con altura ajustable, ideal para contenido extenso.

4. **Select**: 
   - **Formularios**: `FacturaBuscarAvanzada` (campo pagada), `ReservaBuscarAvanzada` (estado)
   - **Descripción**: Lista desplegable para seleccionar una opción entre múltiples valores predefinidos.

5. **RadioSelect**: 
   - **Formularios**: `HotelBuscarAvanzada` (tiene_restaurante)
   - **Descripción**: Botones de radio que permiten seleccionar una única opción de forma visual y directa.

6. **SelectDateWidget**: 
   - **Formularios**: `HuespedForm` (fecha de nacimiento)
   - **Descripción**: Widget que muestra tres listas desplegables separadas para día, mes y año, facilitando la selección de fechas.

