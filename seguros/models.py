from django.db import models
from django.conf import settings
from reservas.models import Reserva  # Referencia externa

class Aseguradora(models.Model):
    """
    Define las aseguradoras y sus planes.
    """
    nombre_aseguradora = models.CharField(max_length=100, verbose_name="Nombre de la Aseguradora / Plan")
    descripcion = models.TextField(verbose_name="Descripción de Coberturas")
    precio_diario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio por Día")
    estado = models.BooleanField(default=True, verbose_name="¿Activa?")

    class Meta:
        verbose_name = "Aseguradora"
        verbose_name_plural = "Aseguradoras"

    def __str__(self):
        return f"{self.nombre_aseguradora} (${self.precio_diario}/día)"


class Poliza(models.Model):
    """
    Representa la póliza emitida a un usuario para una reserva.
    Equivale a la entidad 'seguro_viaje'.
    """
    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        related_name="poliza_seguro",
        verbose_name="Reserva Asociada",
        null=True,
        blank=True
    )
    aseguradora = models.ForeignKey(
        Aseguradora,
        on_delete=models.PROTECT,
        related_name="polizas",
        verbose_name="Aseguradora Asociada"
    )
    numero_poliza = models.CharField(max_length=50, unique=True, verbose_name="Número de Póliza")
    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Emisión")
    costo_seguro = models.DecimalField(max_digits=12, decimal_places=2, editable=False, verbose_name="Costo de Seguro")

    class Meta:
        db_table = "seguros_poliza"
        verbose_name = "Póliza Emitida"
        verbose_name_plural = "Pólizas Emitidas"

    def save(self, *args, **kwargs):
        # Lógica de Negocio (Fat Model): Calcular costo total basado en los días de viaje
        if self.reserva and self.aseguradora:
            dias = self.reserva.paquete.dias_duracion
            self.costo_seguro = self.aseguradora.precio_diario * dias
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Póliza {self.aseguradora.nombre_aseguradora} para Reserva {self.reserva.id if self.reserva else 'N/A'}"
