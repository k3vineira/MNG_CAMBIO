from django.db import models
from django.conf import settings
from reservas.models import Reserva  # Referencia externa

class Poliza(models.Model):
    """
    Define los tipos de planes de seguros disponibles (ej: Plan Básico, Plan Premium).
    Equivale a la entidad 'poliza' del MER de draw.io.
    """
    nombre_aseguradora = models.CharField(max_length=100, verbose_name="Nombre de la Aseguradora / Plan")
    descripcion = models.TextField(verbose_name="Descripción de Coberturas")
    precio_diario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio por Día")
    estado = models.BooleanField(default=True, verbose_name="¿Póliza Activa?")

    class Meta:
        verbose_name = "Póliza / Plan de Seguro"
        verbose_name_plural = "Pólizas / Planes de Seguro"

    def __str__(self):
        return f"{self.nombre_aseguradora} (${self.precio_diario}/día)"


class SeguroViaje(models.Model):
    """
    Representa la adquisición de un seguro por parte de un usuario para una reserva específica.
    Equivale a la entidad 'seguro_viaje' del MER de draw.io.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seguros_viaje",
        verbose_name="Cliente"
    )
    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        related_name="seguro_viaje",
        verbose_name="Reserva Asociada",
        null=True,
        blank=True
    )
    poliza = models.ForeignKey(
        Poliza,
        on_delete=models.PROTECT,
        related_name="seguros_viaje",
        verbose_name="Póliza Asociada"
    )
    numero_poliza = models.CharField(max_length=50, unique=True, verbose_name="Número de Póliza")
    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Emisión")
    costo_seguro = models.DecimalField(max_digits=12, decimal_places=2, editable=False, verbose_name="Costo de Seguro")

    class Meta:
        verbose_name = "Seguro de Viaje Emitido"
        verbose_name_plural = "Seguros de Viaje Emitidos"

    def save(self, *args, **kwargs):
        # Lógica de Negocio (Fat Model): Calcular costo total basado en los días de viaje
        if self.reserva and self.poliza:
            dias = self.reserva.paquete.dias_duracion
            self.costo_seguro = self.poliza.precio_diario * dias
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Seguro {self.numero_poliza} - {self.usuario.username}"
