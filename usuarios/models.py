"""
Modelos de datos para la gestión de usuarios: Usuario personalizado, Cliente y Guía Turístico.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Rol(models.Model):
    """
    Entidad que define los roles del sistema (ej: Administrador, Cliente, Guía Turístico).
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre del Rol')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser con campos adicionales
    como rol, tipo de documento, teléfono e imagen de perfil.
    """
    class TipoDocumento(models.TextChoices):
        CC = 'CC', 'Cédula de Ciudadanía'
        CE = 'CE', 'Cédula de Extranjería'
        PASAPORTE = 'PASAPORTE', 'Pasaporte'

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario registrado con este correo electrónico.',
        },
        verbose_name='Correo Electrónico'
    )

    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Rol'
    )
    tipo_documento = models.CharField(
        max_length=20,
        choices=TipoDocumento.choices,
        verbose_name='Tipo de Documento'
    )
    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Documento'
    )
    telefono = models.CharField(
        max_length=15,
        verbose_name='Teléfono'
    )
    residencia = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Residencia de Origen'
    )
    imagen_perfil = models.ImageField(
        upload_to='perfiles/',
        null=True,
        blank=True,
        verbose_name='Imagen de Perfil'
    )

    def clean(self):
        """Validación limpia del modelo."""
        super().clean()

    def save(self, *args, **kwargs):
        """
        Asigna automáticamente el rol ADMIN a superusuarios.

        Args:
            *args: Argumentos posicionales adicionales.
            **kwargs: Argumentos de clave-valor adicionales.
        """
        # Garantiza que si es superusuario de Django, tome automáticamente el rol ADMIN
        if self.is_superuser and not self.rol:
            rol_admin, _ = Rol.objects.get_or_create(nombre='ADMIN')
            self.rol = rol_admin

        super().save(*args, **kwargs)

    # --- ALIAS EN ESPAÑOL LATAM ---
    @property
    def nombre_usuario(self):
        """Alias en español LATAM para username."""
        return self.username

    @nombre_usuario.setter
    def nombre_usuario(self, value):
        self.username = value

    @property
    def nombres(self):
        """Alias en español LATAM para first_name."""
        return self.first_name

    @nombres.setter
    def nombres(self, value):
        self.first_name = value

    @property
    def apellidos(self):
        """Alias en español LATAM para last_name."""
        return self.last_name

    @apellidos.setter
    def apellidos(self, value):
        self.last_name = value

    @property
    def es_activo(self):
        """Alias en español LATAM para is_active."""
        return self.is_active

    @es_activo.setter
    def es_activo(self, value):
        self.is_active = value

    @property
    def es_personal(self):
        """Alias en español LATAM para is_staff."""
        return self.is_staff

    @es_personal.setter
    def es_personal(self, value):
        self.is_staff = value

    @property
    def es_superusuario(self):
        """Alias en español LATAM para is_superuser."""
        return self.is_superuser

    @es_superusuario.setter
    def es_superusuario(self, value):
        self.is_superuser = value

    @property
    def fecha_registro(self):
        """Alias en español LATAM para date_joined."""
        return self.date_joined

    @property
    def ultimo_login(self):
        """Alias en español LATAM para last_login."""
        return self.last_login

    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def avatar_url(self):
        """Retorna la URL de la imagen o una por defecto si no existe."""
        if self.imagen_perfil and hasattr(self.imagen_perfil, 'url'):
            return self.imagen_perfil.url
        return f"{settings.STATIC_URL}img/avatar_pred.webp"

    @property
    def es_guia(self):
        """Retorna si el usuario tiene el rol de Guía Turístico."""
        return self.rol and self.rol.nombre == 'GUIA'

    @property
    def es_turista(self):
        """Retorna si el usuario tiene el rol de Cliente / Turista."""
        return self.rol and self.rol.nombre == 'CLIENTE'

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        """Retorna el nombre de usuario y su rol como representación textual."""
        return f"{self.username} - {self.rol}"


class Cliente(models.Model):
    """
    Perfil extendido para usuarios con rol de Cliente/Turista.
    Asociado mediante una relación uno-a-uno con el modelo Usuario.
    """
    # Relación uno a uno que mapea "USUARIO es un CLIENTE"
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='cliente',
        verbose_name='Cuenta de Usuario'
    )
    pais = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='País'
    )
    departamento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Departamento'
    )
    ciudad = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Ciudad'
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        """Retorna el nombre completo del cliente como representación textual."""
        return self.usuario.nombre_completo


class GuiaTuristico(models.Model):
    """
    Perfil extendido para usuarios con rol de Guía Turístico.
    Asociado mediante una relación uno-a-uno con el modelo Usuario.
    """
    # Relación uno a uno que mapea "USUARIO es un GUIA_TURISTICO"
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='guia',
        verbose_name='Cuenta de Usuario'
    )
    numero_tarjeta_profesional = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Licencia de Turismo'
    )
    experiencia_anos = models.PositiveIntegerField(
        default=0,
        verbose_name='Años de Experiencia'
    )
    experiencia_fecha = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Inicio de Experiencia'
    )
    descripcion_experiencia = models.TextField(
        blank=True,
        verbose_name='Descripción de la Experiencia'
    )
    entidad_salud = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Entidad de Salud'
    )

    class Meta:
        verbose_name = 'Guía Turístico'
        verbose_name_plural = 'Guías Turísticos'

    def __str__(self):
        """Retorna 'Guía:' seguido del nombre completo del usuario."""
        return f"Guía: {self.usuario.nombre_completo}"
