"""
Modelos de datos para las promociones y banners publicitarios del sitio.
"""

from django.db import models
from catalogo.models import Paquete, Tarifa

class Promocion(models.Model):
    """Promoción o descuento aplicado a un paquete turístico durante un período determinado."""
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

class PaquetePromocion(models.Model):
    """
    Entidad intermedia que asocia un Paquete, una Promocion y una Tarifa.
    Equivale a la tabla intermedia 'paquete_promociones' del MER.
    """
    paquete = models.ForeignKey(
        Paquete,
        on_delete=models.CASCADE,
        related_name='paquete_promociones',
        verbose_name='Paquete'
    )
    promocion = models.ForeignKey(
        Promocion,
        on_delete=models.CASCADE,
        related_name='paquete_promociones',
        verbose_name='Promoción'
    )
    class Meta:
        db_table = 'paquete_promociones'
        verbose_name = 'Paquete Promoción'
        verbose_name_plural = 'Paquetes Promociones'

    def __str__(self):
        return f"{self.paquete.nombre} - {self.promocion.nombre}"

