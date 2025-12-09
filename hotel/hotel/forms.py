from django import forms
from django.forms import ModelForm
from .models import *
import datetime
from django.contrib.auth.forms import UserCreationForm

# Ahora vamos a definir nuestro formulario para el modelo Huespued (Model Forms)

class HuespedForm(ModelForm):
    class Meta:

        model = Huesped
        fields = "__all__"
        labels = {
            "nombre": ("Nombre Huesped"),
            "apellido": ("Apellido Huesped"),
            "correo": ("Correo Huesped"),
            "telefono": ("Telefono Huesped"),
            "fecha_nacimiento": ("Fecha Nacimiento Huesped"),
        }
        help_texts = {
            "nombre": ("80 caracteres como maximo"),
            "apellido": ("80 caracteres como maximo")
        }
        widgets = {
            "fecha_nacimiento":forms.SelectDateWidget(years=range(1920, 2025))
        }
        localized_fields = ["fecha_nacimiento"]
        
    def clean(self):

        #Validaciones basicas de todos mis modelos usando clean 
        super().clean()

        #Obtenemos los campos para hacer validaciones personalizadas
        nombre = self.cleaned_data.get('nombre')
        telefono = self.cleaned_data.get('telefono')

        #Personalizamos validaciones
        if len(nombre) < 3:
            self.add_error('nombre','El nombre debe tener al menos 3 caracteres.')

        if len(telefono) < 9:
            self.add_error('telefono','El telefono debe de tener 9 numeros.')

        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data


# -----------------------------------------------------------------------------
# HOTEL IMAGE
# -----------------------------------------------------------------------------
class HotelImageForm(ModelForm):
    class Meta:
        model = HotelImage
        fields = ['hotel', 'imagen']
        labels = {
            "hotel": "Hotel",
            "imagen": "Imagen del Hotel",
        }
        widgets = {
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
        }
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            # Validar que sea una imagen
            if not imagen.content_type.startswith('image/'):
                raise forms.ValidationError('El archivo debe ser una imagen.')
            # Validar tamaño (máximo 5MB)
            if imagen.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La imagen no puede superar los 5MB.')
        return imagen

# -----------------------------------------------------------------------------
# HOTEL
# -----------------------------------------------------------------------------
class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = "__all__"
        labels = {
            "nombre": ("Nombre del Hotel"),
            "descripcion": ("Descripción"),
            "direccion": ("Dirección"),
            "fecha_fundacion": ("Fecha de Fundación"),
            "calificacion": ("Calificación"),
            "num_habitaciones": ("Número de Habitaciones"),
            "tiene_restaurante": ("¿Tiene Restaurante?"),
            "correo_contacto": ("Correo de Contacto"),
            "sitio_web": ("Sitio Web"),
            "hora_apertura": ("Hora de Apertura"),
            "servicios": ("Servicios"),
        }
        widgets = {
            "fecha_fundacion": forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            "hora_apertura": forms.TimeInput(attrs={'type': 'time'}),
            "descripcion": forms.Textarea(attrs={'rows': 3}),
        }
        localized_fields = ["fecha_fundacion"]

    def clean(self):
        super().clean()
        num_habitaciones = self.cleaned_data.get('num_habitaciones')
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) < 3:
            self.add_error('nombre', 'El nombre debe tener al menos 3 caracteres.')
        if num_habitaciones and num_habitaciones > 100:
            self.add_error('num_habitaciones', 'Los hoteles no pueden tener más de 100 habitaciones.')
        return self.cleaned_data

class HotelBuscarAvanzada(forms.Form):
    nombre_contiene = forms.CharField(
        label='Nombre contiene',
        required=False,
        help_text="(Opcional)"
    )
    calificacion_minima = forms.DecimalField(
        label='Calificación mínima',
        required=False,
        decimal_places=2,
        help_text="(Opcional)"
    )
    tiene_restaurante = forms.NullBooleanField(
        label='¿Tiene restaurante?',
        required=False,
        widget=forms.RadioSelect(choices=[
            (None, 'Indiferente'),
            (True, 'Sí'),
            (False, 'No')
        ]),
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        nombre_contiene = self.cleaned_data.get('nombre_contiene')
        calificacion_minima = self.cleaned_data.get('calificacion_minima')
        tiene_restaurante = self.cleaned_data.get('tiene_restaurante')

        if not any([nombre_contiene, calificacion_minima, tiene_restaurante is not None]):
            self.add_error('nombre_contiene', 'Debe rellenar al menos un campo.')
        if(
            calificacion_minima and calificacion_minima < 0
            ):
            self.add_error('calificacion_minima','La calificacion debe ser mayor que cero.')
        
        return self.cleaned_data

# -----------------------------------------------------------------------------
# CONTACTO HOTEL
# -----------------------------------------------------------------------------
class ContactoHotelForm(ModelForm):
    class Meta:
        model = ContactoHotel
        fields = "__all__"
        labels = {
            "nombre_contacto": ("Nombre del Contacto"),
            "telefono": ("Teléfono"),
            "correo": ("Correo Electrónico"),
            "sitio_web": ("Sitio Web"),
            "hotel": ("Hotel Asociado"),
        }
    
    def clean(self):
        super().clean()
        nombre_contacto = self.cleaned_data.get('nombre_contacto')
        if nombre_contacto and len(nombre_contacto) < 3:
            self.add_error('nombre_contacto', 'El nombre debe tener al menos 3 caracteres.')
        
        telefono = self.cleaned_data.get('telefono')
        if telefono and len(telefono) < 9:
            self.add_error('telefono', 'El teléfono debe tener al menos 9 dígitos.')
        return self.cleaned_data

class ContactoHotelBuscarAvanzada(forms.Form):
    nombre_contacto_contiene = forms.CharField(
        label='Nombre contacto contiene',
        required=False,
        help_text="(Opcional)"
    )
    correo_contiene = forms.CharField(
        label='Correo contiene',
        required=False,
        help_text="(Opcional)"
    )
    telefono_contiene = forms.CharField(
        label='Teléfono contiene',
        required=False,
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        nombre_contacto_contiene = self.cleaned_data.get('nombre_contacto_contiene')
        correo_contiene = self.cleaned_data.get('correo_contiene')
        telefono_contiene = self.cleaned_data.get('telefono_contiene')

        if not any([nombre_contacto_contiene, correo_contiene, telefono_contiene]):
            self.add_error('nombre_contacto_contiene', 'Debe rellenar al menos un campo.')
        if(
            correo_contiene and len(correo_contiene) < 0
            ):
            self.add_error('correo_contiene','El numero de caracteres del correo debe ser mayor que cero.')
        return self.cleaned_data

# -----------------------------------------------------------------------------
# PERFIL HUESPED
# -----------------------------------------------------------------------------
class PerfilHuespedForm(ModelForm):
    class Meta:
        model = PerfilHuesped
        fields = "__all__"
        labels = {
            "huesped": ("Huésped"),
            "nacionalidad": ("Nacionalidad"),
            "numero_pasaporte": ("Número de Pasaporte"),
            "puntos_fidelidad": ("Puntos de Fidelidad"),
            "preferencias": ("Preferencias"),
        }
        widgets = {
            "preferencias": forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        super().clean()
        nacionalidad = self.cleaned_data.get('nacionalidad')
        if nacionalidad and len(nacionalidad) < 3:
            self.add_error('nacionalidad', 'La nacionalidad debe tener al menos 3 caracteres.')
            
        puntos = self.cleaned_data.get('puntos_fidelidad')
        if puntos is not None and puntos < 0:
            self.add_error('puntos_fidelidad', 'Los puntos no pueden ser negativos.')
        return self.cleaned_data

class PerfilHuespedBuscarAvanzada(forms.Form):
    nacionalidad_contiene = forms.CharField(
        label='Nacionalidad contiene',
        required=False,
        help_text="(Opcional)"
    )
    puntos_minimos = forms.IntegerField(
        label='Puntos mínimos',
        required=False,
        min_value=0,
        help_text="(Opcional)"
    )
    numero_pasaporte_contiene = forms.CharField(
        label='Número pasaporte contiene',
        required=False,
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        nacionalidad_contiene = self.cleaned_data.get('nacionalidad_contiene')
        puntos_minimos = self.cleaned_data.get('puntos_minimos')
        numero_pasaporte_contiene = self.cleaned_data.get('numero_pasaporte_contiene')

        if not any([nacionalidad_contiene, puntos_minimos is not None, numero_pasaporte_contiene]):
            self.add_error('nacionalidad_contiene', 'Debe rellenar al menos un campo.')
        if(
            puntos_minimos and puntos_minimos < 0
            ):
            self.add_error('puntos_minimos','El numero de puntos debe ser mayor que cero.')
        return self.cleaned_data

# -----------------------------------------------------------------------------
# RESERVA
# -----------------------------------------------------------------------------
class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = "__all__"
        # Excluimos 'creada_en' porque es auto_now_add y no editable
        exclude = ['creada_en']
        labels = {
            "huesped": ("Huésped"),
            "habitacion": ("Habitación"),
            "fecha_entrada": ("Fecha de Entrada"),
            "fecha_salida": ("Fecha de Salida"),
            "estado": ("Estado"),
        }
        widgets = {
            "fecha_entrada": forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            "fecha_salida": forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        localized_fields = ["fecha_entrada", "fecha_salida"]

    def clean(self):
        super().clean()
        fecha_entrada = self.cleaned_data.get('fecha_entrada')
        fecha_salida = self.cleaned_data.get('fecha_salida')

        if fecha_entrada and fecha_salida and fecha_salida < fecha_entrada:
            self.add_error('fecha_salida', 'La fecha de salida no puede ser anterior a la de entrada.')
            
        if fecha_entrada and fecha_entrada < datetime.date.today():
             self.add_error('fecha_entrada', 'La fecha de entrada no puede ser en el pasado.')
        return self.cleaned_data

class ReservaBuscarAvanzada(forms.Form):
    huesped_nombre = forms.CharField(
        label='Nombre Huésped contiene',
        required=False,
        help_text="(Opcional)"
    )
    fecha_entrada_desde = forms.DateField(
        label='Fecha entrada desde',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="(Opcional)"
    )
    estado = forms.ChoiceField(
        label='Estado',
        choices=[('', 'Cualquiera')] + Reserva.ESTADOS,
        required=False,
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        huesped_nombre = self.cleaned_data.get('huesped_nombre')
        fecha_entrada_desde = self.cleaned_data.get('fecha_entrada_desde')
        estado = self.cleaned_data.get('estado')

        if not any([huesped_nombre, fecha_entrada_desde, estado]):
            self.add_error('huesped_nombre', 'Debe rellenar al menos un campo.')
        if(
            huesped_nombre and len(huesped_nombre) < 0
            ):
            self.add_error('huesped_nombre','El numero de caracteres del nombre debe ser mayor que cero.')
        return self.cleaned_data

# -----------------------------------------------------------------------------
# FACTURA
# -----------------------------------------------------------------------------
class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        fields = "__all__"
        # 'emitida_en' es auto_now_add
        exclude = ['emitida_en'] 
        labels = {
            "reserva": ("Reserva"),
            "numero_factura": ("Número de Factura"),
            "monto_total": ("Monto Total"),
            "pagada": ("¿Pagada?"),
            "notas": ("Notas"),
        }
        widgets = {
            "notas": forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        super().clean()
        monto_total = self.cleaned_data.get('monto_total')
        if monto_total and monto_total < 0:
            self.add_error('monto_total', 'El monto no puede ser negativo.')
            
        numero = self.cleaned_data.get('numero_factura')
        if numero and len(numero) < 5:
            self.add_error('numero_factura', 'El número de factura debe tener al menos 5 caracteres.')
        return self.cleaned_data

class FacturaBuscarAvanzada(forms.Form):
    numero_contiene = forms.CharField(
        label='Número factura contiene',
        required=False,
        help_text="(Opcional)"
    )
    monto_minimo = forms.DecimalField(
        label='Monto mínimo',
        required=False,
        decimal_places=2,
        help_text="(Opcional)"
    )
    pagada = forms.NullBooleanField(
        label='¿Pagada?',
        required=False,
        widget=forms.Select(choices=[
            (None, 'Indiferente'),
            (True, 'Sí'),
            (False, 'No')
        ]),
        help_text="(Opcional)"
    )

    def clean(self):
        super().clean()
        numero_contiene = self.cleaned_data.get('numero_contiene')
        monto_minimo = self.cleaned_data.get('monto_minimo')
        pagada = self.cleaned_data.get('pagada')

        if not any([numero_contiene, monto_minimo is not None, pagada is not None]):
            self.add_error('numero_contiene', 'Debe rellenar al menos un campo.')
            self.add_error('monto_minimo', 'Debe rellenar al menos un campo.')
            self.add_error('pagada', 'Debe rellenar al menos un campo.')
        if(
            monto_minimo and monto_minimo < 0
            ):
            self.add_error('monto_minimo','El monto minimo debe ser mayor que cero.')
        return self.cleaned_data

class HuespedBuscarAvanzada(forms.Form):

    nombre_huesped_contiene = forms.CharField(
        label='Nombre de huesped contiene',
        help_text="(Opcional)",
        required=False
    )

    fecha_nacimiento_desde = forms.DateField(
        label='nacimiento desde',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateInput(attrs={'type':'date'})
    )

    fecha_nacimiento_hasta = forms.DateField(
        label='nacimiento hasta',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateInput(attrs={'type':'date'})
    )

    def clean(self):

        #Validamos con el modelo actual
        super().clean()

        #Obtenemos los campos
        nombre_huesped_contiene = self.cleaned_data.get('nombre_huesped_contiene')
        fecha_nacimiento_desde = self.cleaned_data.get('fecha_nacimiento_desde')
        fecha_nacimiento_hasta = self.cleaned_data.get('fecha_nacimiento_hasta')
        
        #Comprobamos
        if(
            nombre_huesped_contiene == "" and
            fecha_nacimiento_desde is None and
            fecha_nacimiento_hasta is None
        ):
            self.add_error('nombre_huesped_contiene','Debe de rellenar al menos un campo.')
            self.add_error('fecha_nacimiento_desde','Debe de rellenar al menos un campo.')
            self.add_error('fecha_nacimiento_hasta','Debe de rellenar al menos un campo.')
        
        if(
            not fecha_nacimiento_desde is None and
            not fecha_nacimiento_hasta is None and
            fecha_nacimiento_hasta < fecha_nacimiento_desde
            ):
            self.add_error('fecha_nacimiento_desde','Rango de fecha no valido.')
            self.add_error('fecha_nacimiento_hasta','Rango de fecha no valido.')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
    
class RegistroForm(UserCreationForm):
    
    roles = (
        (Usuario.HUESPED, 'huésped'),
        (Usuario.GESTOR, 'gestor'),
    )
    
    rol = forms.ChoiceField(choices=roles)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'rol']
