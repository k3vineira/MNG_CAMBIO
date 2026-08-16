from django.db import models
from django.conf import settings
from reservas.models import Reserva  # Referencia externa

class SeguroViaje(models.Model):
    """
    Define los tipos de planes de seguros disponibles (ej: Plan Básico, Plan Premium).
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Plan")
    descripcion = models.TextField(verbose_name="Descripción de Coberturas")
    precio_diario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio por Día")
    activo = models.BooleanField(default=True, verbose_name="¿Plan Activo?")

    class Meta:
        verbose_name = "Seguro de Viaje"
        verbose_name_plural = "Seguros de Viaje"

    def __str__(self):
        return f"{self.nombre} (${self.precio_diario}/día)"


class Poliza(models.Model):
    """
    Representa la adquisición de un seguro por parte de un usuario para una reserva específica.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="polizas",
        verbose_name="Cliente"
    )
    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        related_name="poliza_seguro",
        verbose_name="Reserva Asociada",
        null=True,
        blank=True
    )
    seguro = models.ForeignKey(
        SeguroViaje,
        on_delete=models.PROTECT,
        verbose_name="Plan de Seguro"
    )
    codigo_poliza = models.CharField(max_length=50, unique=True, verbose_name="Código de Póliza")
    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Emisión")
    costo_total = models.DecimalField(max_digits=12, decimal_places=2, editable=False, verbose_name="Costo Total")

    class Meta:
        verbose_name = "Póliza de Seguro"
        verbose_name_plural = "Pólizas de Seguro"

    def save(self, *args, **kwargs):
        # Lógica de Negocio (Fat Model): Calcular costo total basado en los días de viaje
        if self.reserva and self.seguro:
            # Asumiendo que la reserva tiene días de duración (ej: paquete.dias_duracion)
            dias = self.reserva.paquete.dias_duracion
            self.costo_total = self.seguro.precio_diario * dias
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Póliza {self.codigo_poliza} - {self.usuario.username}"
