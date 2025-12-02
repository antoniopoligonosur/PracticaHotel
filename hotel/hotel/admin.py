from django.contrib import admin
from .models import Hotel, ContactoHotel, TipoHabitacion, Habitacion, Huesped, Servicio

# Register your models here.

admin.site.register(Hotel)
admin.site.register(ContactoHotel)
admin.site.register(TipoHabitacion)
admin.site.register(Habitacion)
admin.site.register(Huesped)
admin.site.register(Servicio)