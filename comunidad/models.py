"""
Modelos de datos para la comunidad: Calificaciones, Blog, PQRS y Seguimiento.
"""

from django.db import models
from django.urls import reverse
from django.conf import settings


class Calificacion(models.Model):
    """
    Calificación y reseña de una experiencia o reserva de un paquete turístico
    realizada por un cliente o usuario registrado.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='calificaciones',
        verbose_name='Usuario / Cliente'
    )
    paquete = models.ForeignKey(
        'catalogo.Paquete',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calificaciones',
        verbose_name='Paquete Turístico'
    )
    reserva = models.ForeignKey(
        'reservas.Reserva',
        on_delete=models.SET_NULL,
        related_name='calificaciones',
        verbose_name='Reserva Calificada',
        null=True,
        blank=True
    )
    tipo = models.CharField(
        max_length=20,
        default='experiencia',
        verbose_name='Tipo',
        help_text='Tipo de reseña: experiencia, pregunta, etc.'
    )
    titulo = models.CharField(
        max_length=255,
        verbose_name='Título'
    )
    puntaje_estrellas = models.PositiveSmallIntegerField(
        default=5,
        verbose_name='Puntaje / Estrellas'
    )
    comentario = models.TextField(
        verbose_name='Comentario / Reseña'
    )
    visible = models.BooleanField(
        default=True,
        verbose_name='¿Visible?'
    )
    admin_respuesta = models.TextField(
        blank=True,
        null=True,
        verbose_name='Respuesta del Admin'
    )
    fecha_calificacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Calificación'
    )

    # Aliases de retrocompatibilidad
    @property
    def valoracion(self):
        """Alias para puntaje_estrellas."""
        return self.puntaje_estrellas

    @valoracion.setter
    def valoracion(self, value):
        self.puntaje_estrellas = value

    @property
    def mensaje(self):
        """Alias para comentario."""
        return self.comentario

    @mensaje.setter
    def mensaje(self, value):
        self.comentario = value

    @property
    def fecha_creacion(self):
        """Alias para fecha_calificacion."""
        return self.fecha_calificacion

    class Meta:
        db_table = 'comunidad_calificacion'
        ordering = ['-fecha_calificacion']
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'

    def __str__(self):
        """Retorna el usuario y título/paquete de la calificación como representación textual."""
        nombre_usuario = self.usuario.username if self.usuario else "Anónimo"
        return f"Calificación de {nombre_usuario} ({self.puntaje_estrellas}★) - {self.titulo or (self.paquete.nombre if self.paquete else 'General')}"


class Blog(models.Model):
    """Entrada de blog publicada por un administrador o autor en Mongua Turismo."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blogs_publicados",
        verbose_name="Autor / Administrador",
    )
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    informacion_adicional = models.TextField(blank=True)
    imagen_destacada = models.ImageField(upload_to="blog/", blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(
        default=True, verbose_name="¿Está Publicado?"
    )

    class Meta:
        ordering = ["-fecha_publicacion"]
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def get_absolute_url(self):
        """Retorna la URL de detalle de este post del blog."""
        return reverse("detalle_blog", kwargs={"id": self.id})

    def __str__(self):
        """Retorna el título y el autor del blog."""
        return f"{self.titulo} - Por: {self.usuario.get_full_name() or self.usuario.username}"


class PQRS(models.Model):
    """Solicitud de Petición, Queja, Reclamo o Sugerencia enviada por un usuario."""

    TIPO_CHOICES = [
        ('peticion', 'Petición'),
        ('queja', 'Queja'),
        ('reclamo', 'Reclamo'),
        ('sugerencia', 'Sugerencia'),
    ]
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('en_proceso', 'En Proceso'),
        ('cerrado', 'Cerrado'),
    ]
    cliente = models.ForeignKey(
        'usuarios.Cliente',
        on_delete=models.CASCADE,
        related_name='pqrs',
        null=True,
        blank=True,
    )
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(
        max_length=15, choices=ESTADO_CHOICES, default='abierto'
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'PQRS'

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.asunto}'


class Seguimiento(models.Model):
    """Registro de seguimiento y respuestas a una solicitud PQRS por parte de un usuario o administrador."""
    pqrs = models.ForeignKey(PQRS, on_delete=models.CASCADE, related_name='seguimientos')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seguimientos',
        null=True,
        blank=True,
        verbose_name='Usuario / Administrador'
    )
    respuesta = models.TextField(verbose_name='Mensaje / Respuesta')
    fecha_respuesta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Respuesta')

    class Meta:
        db_table = 'seguimiento'
        ordering = ['fecha_respuesta']
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'

    def __str__(self):
        return f'Seguimiento de {self.pqrs} - {self.fecha_respuesta.strftime("%Y-%m-%d %H:%M:%S")}'


# Aliases de retrocompatibilidad
Resena = Calificacion
Comentario = Calificacion
