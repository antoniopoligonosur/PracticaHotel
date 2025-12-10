from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from hotel.models import Hotel, Habitacion, Huesped, Reserva, Factura, ContactoHotel, PerfilHuesped, Servicio, TipoHabitacion

class Command(BaseCommand):
    help = 'Configura los permisos para los grupos Gestor y Huesped'

    def handle(self, *args, **kwargs):
        # Crear grupos
        grupo_gestor, _ = Group.objects.get_or_create(name='Gestor')
        grupo_huesped, _ = Group.objects.get_or_create(name='Huesped')

        # Modelos para Gestor (Gestión completa)
        modelos_gestor = [Hotel, Habitacion, Huesped, Reserva, Factura, ContactoHotel, PerfilHuesped, Servicio, TipoHabitacion]
        permisos_gestor = ['add', 'change', 'delete', 'view']

        for modelo in modelos_gestor:
            content_type = ContentType.objects.get_for_model(modelo)
            for accion in permisos_gestor:
                codename = f'{accion}_{modelo._meta.model_name}'
                try:
                    permiso = Permission.objects.get(codename=codename, content_type=content_type)
                    grupo_gestor.permissions.add(permiso)
                    self.stdout.write(self.style.SUCCESS(f'Permiso {codename} agregado a Gestor'))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Permiso {codename} no encontrado'))

        # Modelos para Huesped (Solo Reserva y visualización limitada)
        # Huesped puede crear y ver Reservas. NO puede ver Hoteles (en el sentido de admin/gestión), 
        # pero la vista pública de hoteles no requiere permisos de 'view_hotel' de django.contrib.auth 
        # a menos que se proteja explícitamente con permission_required.
        # Asumimos que permission_required('hotel.view_hotel') no se usa en la parte pública.
        
        # Permisos explícitos solicitados: add, view sobre Reservas.
        modelos_huesped = [Reserva]
        permisos_huesped = ['add', 'view']

        for modelo in modelos_huesped:
            content_type = ContentType.objects.get_for_model(modelo)
            for accion in permisos_huesped:
                codename = f'{accion}_{modelo._meta.model_name}'
                try:
                    permiso = Permission.objects.get(codename=codename, content_type=content_type)
                    grupo_huesped.permissions.add(permiso)
                    self.stdout.write(self.style.SUCCESS(f'Permiso {codename} agregado a Huesped'))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Permiso {codename} no encontrado'))

        self.stdout.write(self.style.SUCCESS('Permisos configurados correctamente'))
