from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Hotel, ContactoHotel, TipoHabitacion, Habitacion, Huesped, PerfilHuesped, Servicio, Reserva, Factura, ReservaServicio, Usuario, Gestor, HotelImage

# Register your models here.

admin.site.register(Usuario, UserAdmin)
admin.site.register(Gestor)
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
admin.site.register(HotelImage)