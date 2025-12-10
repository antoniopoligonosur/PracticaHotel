from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from hotel.models import Hotel, Habitacion, Reserva, Factura, ContactoHotel, PerfilHuesped, Huesped, Gestor

class Command(BaseCommand):
    help = 'Crea los grupos de usuarios y asigna sus permisos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando creación de grupos y permisos...'))

        # Definición de grupos y sus permisos
        grupos_permisos = {
            'Administrador': {
                'models': [Hotel, Habitacion, Reserva, Factura, ContactoHotel, PerfilHuesped, Huesped, Gestor],
                'permissions': ['add', 'change', 'delete', 'view']
            },
            'Gestor': {
                'models': [Hotel, Habitacion, ContactoHotel],
                'permissions': ['add', 'change', 'delete', 'view']
            },
            'Huesped': {
                'models': [Reserva, Factura],
                'permissions': ['add', 'view'] # Huespedes pueden crear y ver reservas, ver facturas
            }
        }

        for nombre_grupo, config in grupos_permisos.items():
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)
            if created:
                self.stdout.write(f'Grupo "{nombre_grupo}" creado.')
            else:
                self.stdout.write(f'Grupo "{nombre_grupo}" ya existía.')

            # Limpiar permisos anteriores para asegurar estado limpio
            grupo.permissions.clear()

            for modelo in config['models']:
                content_type = ContentType.objects.get_for_model(modelo)
                for perm_code in config['permissions']:
                    codename = f'{perm_code}_{modelo._meta.model_name}'
                    try:
                        permission = Permission.objects.get(content_type=content_type, codename=codename)
                        grupo.permissions.add(permission)
                        # self.stdout.write(f'  - Permiso {codename} asignado a {nombre_grupo}')
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'  ! Permiso {codename} no encontrado'))

            self.stdout.write(self.style.SUCCESS(f'Permisos actualizados para grupo "{nombre_grupo}"'))

        self.stdout.write(self.style.SUCCESS('¡Proceso de grupos y permisos completado!'))
