"""
Modelos de datos para las promociones y banners publicitarios del sitio.
"""

from django.db import models
from catalogo.models import Paquete

class Promocion(models.Model):
    """Promoción o descuento aplicado a un paquete turístico durante un período determinado."""
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name='promociones')
    nombre = models.CharField(max_length=150, verbose_name="Nombre de la promoción")
    descripcion = models.TextField(verbose_name="Descripción")
    descuento = models.PositiveIntegerField(verbose_name="Porcentaje de descuento")
    fecha_fin = models.DateField(verbose_name="Fecha de fin")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    codigo_promocion = models.CharField(max_length=20, unique=True, verbose_name="Código de promoción")
    condiciones = models.TextField(blank=True, null=True, verbose_name="Condiciones")
    codigo_cupon = models.CharField(max_length=30, blank=True, null=True, verbose_name="Código de cupón")
    activa = models.BooleanField(default=True, verbose_name="¿Activa?")

    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"

    def __str__(self):
        """Retorna el nombre y porcentaje de descuento de la promoción."""
        return f"{self.nombre} ({self.descuento}%)"

class Banner(models.Model):
    """Banner publicitario que se muestra en el sitio web con imagen y enlace opcional."""
    imagen = models.ImageField(upload_to='banners/', verbose_name="Imagen del Banner")
    titulo = models.CharField(max_length=150, verbose_name="Título del Banner")
    enlace = models.URLField(blank=True, null=True, verbose_name="Enlace (Opcional)")
    activo = models.BooleanField(default=True, verbose_name="¿Activo?")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        """Retorna el título del banner como representación textual."""
        return self.titulo
