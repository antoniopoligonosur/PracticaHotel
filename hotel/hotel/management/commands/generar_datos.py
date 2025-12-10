from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random
import uuid
from datetime import timedelta, datetime
from decimal import Decimal
from hotel.models import (
    Servicio,
    Hotel,
    ContactoHotel,
    TipoHabitacion,
    Habitacion,
    Huesped,
    PerfilHuesped,
    Reserva,
    ReservaServicio,
    Factura
)

class Command(BaseCommand):
    help = 'Generar 10 datos aleatorios por modelo usando Faker'

    def handle(self, *args, **options):
        fake = Faker('es_ES')
        Faker.seed(0)
        random.seed(0)

        with transaction.atomic():
            # 1. Servicios
            self.stdout.write("Generando usuarios...")
            servicios = []
            for _ in range(10):
                s = Servicio.objects.create(
                    nombre=fake.unique.word().capitalize(),
                    descripcion=fake.sentence(nb_words=8),
                    precio=Decimal(f"{random.uniform(5, 150):.2f}"),
                    es_opcional=fake.boolean(chance_of_getting_true=70),
                    duracion_minutos=random.choice([30, 45, 60, None])
                )
                servicios.append(s)

            # 2. Hoteles
            self.stdout.write("Generando usuarios...")
            hoteles = []
            for _ in range(10):
                h = Hotel.objects.create(
                    nombre=fake.unique.company(),
                    descripcion=fake.text(max_nb_chars=200),
                    direccion=fake.address(),
                    fecha_fundacion=fake.date_between(start_date='-40y', end_date='-1y'),
                    calificacion=Decimal(f"{random.uniform(0, 5):.2f}")
                )
                # añadir algunos servicios aleatorios al hotel
                servicios_aleatorios = random.sample(servicios, random.randint(0, 4))
                h.servicios.set(servicios_aleatorios)
                hoteles.append(h)

            # 3. ContactoHotel (OneToOne con Hotel) - crear solo para algunos hoteles (hasta 10)
            self.stdout.write("Generando usuarios...")
            contactos = []
            for hotel in hoteles:
                c = ContactoHotel.objects.create(
                    hotel=hotel,
                    nombre_contacto=fake.name(),
                    telefono=fake.unique.phone_number(),
                    correo=fake.unique.company_email(),
                    sitio_web=fake.url()
                )
                contactos.append(c)

            # 4. TipoHabitacion
            self.stdout.write("Generando usuarios...")
            tipos = []
            for _ in range(6):
                t = TipoHabitacion.objects.create(
                    nombre=fake.word().capitalize(),
                    descripcion=fake.sentence(nb_words=6),
                    capacidad=random.randint(1, 6),
                    precio_base=Decimal(f"{random.uniform(30, 400):.2f}")
                )
                tipos.append(t)
# ... (código anterior igual) ...

            # 5. Habitaciones (FK a TipoHabitacion y Hotel) + ManyToMany servicios
            self.stdout.write("Generando habitaciones...") # Corregido mensaje también
            habitaciones = []
            for _ in range(30):
                hotel = random.choice(hoteles)
                tipo = random.choice(tipos)
                numero = str(random.randint(1, 999))
                h_obj = Habitacion.objects.create(
                    numero=numero,
                    piso=random.randint(0, 10),
                    tipo=tipo,
                    hotel=hotel,
                    disponible=fake.boolean(chance_of_getting_true=80)
                    # SE ELIMINÓ LA LÍNEA: imagen_url="/imagen"
                )
                # servicios de la habitación
                servicios_hab = random.sample(servicios, random.randint(0, 3))
                h_obj.servicios.set(servicios_hab)
                habitaciones.append(h_obj)

            # ... (resto del código igual) ...

            # 6. Huespedes
            self.stdout.write("Generando usuarios...")
            huespedes = []
            for _ in range(15):
                email = fake.unique.email()
                hu = Huesped.objects.create(
                    nombre=fake.first_name(),
                    apellido=fake.last_name(),
                    correo=email,
                    telefono=fake.phone_number(),
                    fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=80)
                )
                huespedes.append(hu)

            # 7. PerfilHuesped (OneToOne con Huesped)
            self.stdout.write("Generando usuarios...")
            perfiles = []
            for huesped in huespedes:
                # algunos huéspedes pueden no tener pasaporte (null=True)
                passport = fake.unique.bothify(text='??######') if random.choice([True, False, True]) else None
                p = PerfilHuesped.objects.create(
                    huesped=huesped,
                    nacionalidad=fake.country(),
                    numero_pasaporte=passport,
                    puntos_fidelidad=random.randint(0, 5000),
                    preferencias=fake.sentence(nb_words=6)
                )
                perfiles.append(p)

            # 8. Reservas (cada una necesita huesped y habitacion)
            self.stdout.write("Generando usuarios...")
            reservas = []
            for _ in range(20):
                huesped = random.choice(huespedes)
                habitacion = random.choice(habitaciones)
                fecha_entrada = fake.date_between(start_date='-90d', end_date='today')
                # asegurar salida posterior
                dias = random.randint(1, 10)
                fecha_salida = fecha_entrada + timedelta(days=dias)

                estado = random.choice(['P', 'C', 'F', 'X'])
                r = Reserva.objects.create(
                    huesped=huesped,
                    habitacion=habitacion,
                    fecha_entrada=fecha_entrada,
                    fecha_salida=fecha_salida,
                    estado=estado
                )
                reservas.append(r)

            # 9. ReservaServicio (tabla intermedia con atributos extra)
            self.stdout.write("Generando usuarios...")
            reservaservicios = []
            for reserva in reservas:
                # asignar entre 0 y 4 servicios distintos a la reserva
                servicios_para_reserva = random.sample(servicios, random.randint(0, 4))
                for serv in servicios_para_reserva:
                    cantidad = random.randint(1, 5)
                    precio_en_momento = serv.precio  # podríamos variar un poco
                    nota = fake.sentence(nb_words=6) if random.choice([True, False]) else ''
                    rs = ReservaServicio.objects.create(
                        reserva=reserva,
                        servicio=serv,
                        cantidad=cantidad,
                        precio_en_momento=precio_en_momento,
                        nota=nota
                    )
                    reservaservicios.append(rs)

            # 10. Facturas (OneToOne con Reserva) - crear factura para algunas reservas
            self.stdout.write("Generando usuarios...")
            facturas = []
            for reserva in reservas:
                # decidir si esta reserva tiene factura (no todas tienen)
                if random.choice([True, True, False]):
                    # calcular monto_total simple: noches * precio_base + suma servicios
                    noches = (reserva.fecha_salida - reserva.fecha_entrada).days
                    precio_noche = reserva.habitacion.tipo.precio_base
                    total_habitacion = precio_noche * noches
                    total_servicios = Decimal('0.00')
                    rs_qs = ReservaServicio.objects.filter(reserva=reserva)
                    for rs in rs_qs:
                        total_servicios += (rs.precio_en_momento * rs.cantidad)
                    monto_total = (total_habitacion + total_servicios).quantize(Decimal('0.01'))
                    f = Factura.objects.create(
                        reserva=reserva,
                        numero_factura=str(uuid.uuid4()),
                        monto_total=monto_total,
                        pagada=random.choice([True, False]),
                        notas=fake.sentence(nb_words=8)
                    )
                    facturas.append(f)

        self.stdout.write(self.style.SUCCESS('Datos generados correctamente.'))
