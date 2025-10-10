from django.contrib import admin
from .models import Hotel, ContactoHotel, TipoHabitacion, Habitacion, Huesped, PerfilHuesped, Servicio, Reserva, Factura, ReservaServicio

# Register your models here.

admin.site.register(Hotel)
admin.site.register(ContactoHotel)
admin.site.register(TipoHabitacion)
admin.site.register(Habitacion)
admin.site.register(Huesped)
admin.site.register(PerfilHuesped)
admin.site.register(Servicio)
admin.site.register(Reserva)
admin.site.register(Factura)
admin.site.register(ReservaServicio)