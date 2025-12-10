from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import Group
from hotel.models import *
from faker import Faker
import random
from datetime import timedelta, date

class Command(BaseCommand):
    help = 'Genera datos de prueba para la aplicación'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando generación de datos...'))
        fake = Faker('es_ES')

        with transaction.atomic():
            # 1. Crear Usuarios Base
            self.crear_usuarios_base()
            
            # 2. Crear Hoteles y Habitaciones
            hoteles = self.crear_hoteles(fake)
            
            # 3. Crear Huespedes Fake
            huespedes = self.crear_huespedes_fake(fake)
            
            # 4. Crear Reservas y Facturas
            self.crear_reservas(fake, hoteles, huespedes)

        self.stdout.write(self.style.SUCCESS('¡Datos generados correctamente!'))

    def crear_usuarios_base(self):
        self.stdout.write('Creando usuarios base...')
        
        # Admin
        if not Usuario.objects.filter(username='admin').exists():
            admin = Usuario.objects.create_superuser('admin', 'admin@hotel.com', 'admin')
            grupo_admin = Group.objects.get(name='Administrador')
            admin.groups.add(grupo_admin)
            admin.rol = Usuario.ADMINISTRADOR
            admin.save()

        # Gestor
        if not Usuario.objects.filter(username='gestor1').exists():
            gestor = Usuario.objects.create_user('gestor1', 'gestor1@hotel.com', '1234')
            grupo_gestor = Group.objects.get(name='Gestor')
            gestor.groups.add(grupo_gestor)
            gestor.rol = Usuario.GESTOR
            gestor.save()
            Gestor.objects.create(usuario=gestor, especialidad='Dirección Hotelera', fecha_contratacion=date.today())

        # Huesped
        if not Usuario.objects.filter(username='huesped1').exists():
            huesped_user = Usuario.objects.create_user('huesped1', 'huesped1@hotel.com', '1234')
            grupo_huesped = Group.objects.get(name='Huesped')
            huesped_user.groups.add(grupo_huesped)
            huesped_user.rol = Usuario.HUESPED
            huesped_user.save()
            huesped_perfil = Huesped.objects.create(
                usuario=huesped_user, 
                nombre='Juan', 
                apellido='Pérez', 
                correo='huesped1@hotel.com',
                telefono='600123456'
            )
            PerfilHuesped.objects.create(
                huesped=huesped_perfil,
                nacionalidad='Española',
                puntos_fidelidad=100
            )

    def crear_hoteles(self, fake):
        self.stdout.write('Creando hoteles...')
        hoteles = []
        
        # Crear Servicios
        servicios_nombres = ['Wifi', 'Piscina', 'Gimnasio', 'Desayuno', 'Parking', 'Spa']
        servicios_objs = []
        for nombre in servicios_nombres:
            s, _ = Servicio.objects.get_or_create(
                nombre=nombre, 
                defaults={
                    'descripcion': f'Servicio de {nombre}', 
                    'precio': random.randint(10, 50),
                    'es_opcional': random.choice([True, False])
                }
            )
            servicios_objs.append(s)

        # Crear Tipos de Habitación
        tipos = []
        for nombre, cap in [('Individual', 1), ('Doble', 2), ('Suite', 4)]:
            t, _ = TipoHabitacion.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': f'Habitación {nombre}',
                    'capacidad': cap,
                    'precio_base': random.randint(50, 200)
                }
            )
            tipos.append(t)

        for _ in range(5):
            hotel = Hotel.objects.create(
                nombre=fake.company() + " Hotel",
                descripcion=fake.text(),
                direccion=fake.address(),
                fecha_fundacion=fake.date_between(start_date='-50y', end_date='-1y'),
                calificacion=round(random.uniform(3.0, 5.0), 2),
                num_habitaciones=random.randint(10, 50),
                tiene_restaurante=random.choice([True, False]),
                correo_contacto=fake.email(),
                hora_apertura='08:00'
            )
            hotel.servicios.set(random.sample(servicios_objs, k=random.randint(2, 5)))
            
            ContactoHotel.objects.create(
                hotel=hotel,
                nombre_contacto=fake.name(),
                telefono=fake.phone_number()[:15], # Truncate to fit
                correo=fake.email()
            )

            # Crear Habitaciones
            for i in range(1, 11):
                Habitacion.objects.create(
                    numero=f"{random.randint(1,5)}0{i}",
                    piso=random.randint(1, 5),
                    tipo=random.choice(tipos),
                    hotel=hotel,
                    disponible=True
                )
            
            hoteles.append(hotel)
        return hoteles

    def crear_huespedes_fake(self, fake):
        self.stdout.write('Creando huéspedes fake...')
        huespedes = []
        grupo_huesped = Group.objects.get(name='Huesped')
        
        for _ in range(10):
            username = fake.user_name()
            # Ensure unique username
            while Usuario.objects.filter(username=username).exists():
                username = fake.user_name() + str(random.randint(1, 999))
                
            user = Usuario.objects.create_user(username, fake.email(), '1234')
            user.groups.add(grupo_huesped)
            user.rol = Usuario.HUESPED
            user.save()
            
            huesped = Huesped.objects.create(
                usuario=user,
                nombre=fake.first_name(),
                apellido=fake.last_name(),
                correo=user.email,
                telefono=fake.phone_number()[:15]
            )
            
            PerfilHuesped.objects.create(
                huesped=huesped,
                nacionalidad=fake.country(),
                numero_pasaporte=fake.bothify(text='??#######'),
                puntos_fidelidad=random.randint(0, 500)
            )
            huespedes.append(huesped)
        return huespedes

    def crear_reservas(self, fake, hoteles, huespedes):
        self.stdout.write('Creando reservas...')
        for huesped in huespedes:
            for _ in range(random.randint(1, 3)):
                hotel = random.choice(hoteles)
                habitacion = hotel.habitaciones.first() # Simplificación
                
                fecha_ent = fake.date_between(start_date='-1y', end_date='+1y')
                fecha_sal = fecha_ent + timedelta(days=random.randint(1, 7))
                
                reserva = Reserva.objects.create(
                    huesped=huesped,
                    habitacion=habitacion,
                    fecha_entrada=fecha_ent,
                    fecha_salida=fecha_sal,
                    estado=random.choice(['P', 'C', 'F'])
                )
                
                # Factura
                if reserva.estado in ['C', 'F']:
                    Factura.objects.create(
                        reserva=reserva,
                        monto_total=random.randint(100, 1000),
                        pagada=random.choice([True, False])
                    )
