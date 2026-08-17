"""
Modelos de datos para la comunidad: Calificaciones, Blog, PQRS y Comentarios.
"""

from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.


class Calificacion(models.Model):
    """
    Calificación de un paquete turístico realizada por un cliente.
    Solo se permite una calificación por cliente y paquete.
    """
    cliente = models.ForeignKey('usuarios.Cliente', on_delete=models.CASCADE)
    paquete = models.ForeignKey('catalogo.Paquete', on_delete=models.CASCADE)
    puntaje_estrellas = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    fecha_calificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cliente', 'paquete')


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
    # SE ELIMINA EL CAMPO 'respuesta' DIRECTO PARA EVITAR SOBREESCRITURA
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

class Comentario(models.Model):
    """Comentarios y reseñas de experiencias de usuarios."""
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name='Usuario'
    )
    tipo = models.CharField(
        max_length=20,
        default='experiencia',
        verbose_name='Tipo',
        help_text='Tipo de comentario: experiencia, pregunta, etc.'
    )
    titulo = models.CharField(
        max_length=255, blank=True, verbose_name='Título')
    mensaje = models.TextField(verbose_name='Mensaje')
    valoracion = models.PositiveSmallIntegerField(
        default=5, verbose_name='Valoración')
    paquete = models.ForeignKey(
        'catalogo.Paquete',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comentarios',
        verbose_name='Paquete'
    )
    visible = models.BooleanField(default=True, verbose_name='¿Visible?')
    admin_respuesta = models.TextField(
        blank=True, null=True, verbose_name='Respuesta del Admin')
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de Creación')

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        """Retorna el usuario y título del comentario como representación textual."""
        return f"Comentario de {self.usuario.username} - {self.titulo or 'sin título'}"

