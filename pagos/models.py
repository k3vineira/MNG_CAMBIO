"""
Modelo de datos para los comprobantes de pago enviados por los usuarios.
"""

import os
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal


class Pago(models.Model):
    """
    Pago subido por un usuario para verificar el pago de una reserva o multa.
    El administrador puede aprobarlo o rechazarlo.
    """
    ESTADO_CHOICES = [
        ('pendiente',  'Pendiente de revisión'),
        ('aprobado',   'Aprobado'),
        ('rechazado',  'Rechazado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comprobantes',
        verbose_name='Usuario'
    )

    # Vincular con una reserva específica
    reserva = models.OneToOneField(
        'reservas.Reserva',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pago',
        verbose_name='Reserva'
    )

    referencia = models.CharField(
        max_length=100,
        verbose_name='Número de referencia / transacción',
        help_text='Número de comprobante, transacción o referencia bancaria'
    )
    banco_origen = models.CharField(
        max_length=100,
        verbose_name='Banco / medio de pago'
    )
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Monto pagado'
    )
    imagen_comprobante = models.ImageField(
        upload_to='comprobantes/%Y/%m/',
        verbose_name='Imagen del comprobante'
    )
    descripcion = models.TextField(
        verbose_name='Descripción / nota adicional'
    )
    estado_transaccion = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    nota_admin = models.TextField(
        blank=True,
        verbose_name='Nota del administrador'
    )
    fecha_pago = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha exacta del pago bancario'
    )
    fecha_envio = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de envío')
    fecha_revision = models.DateTimeField(
        null=True, blank=True, verbose_name='Fecha de revisión')

    class Meta:
        db_table = 'pago'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_envio']

    def __str__(self):
        """Retorna el ID, usuario y estado del pago como representación textual."""
        return f"Pago #{self.pk} — {self.usuario.username} — {self.get_estado_transaccion_display()}"

    def clean(self):
        super().clean()
        if self.estado_transaccion == 'aprobado':
            if not self.banco_origen:
                raise ValidationError({"banco_origen": "Debe especificar el banco de origen para aprobar el comprobante."})
            if not self.monto:
                raise ValidationError({"monto": "Debe especificar el monto pagado para aprobar el comprobante."})
            if self.reserva and self.monto < self.reserva.monto_total:
                raise ValidationError({"monto": "El monto pagado no puede ser menor al monto total de la reserva."})
        elif self.estado_transaccion == 'rechazado':
            if not self.nota_admin:
                raise ValidationError({"nota_admin": "Debe justificar el rechazo añadiendo una nota del administrador."})

        if self.monto is not None and self.monto < 0:
            raise ValidationError({"monto": "El monto pagado no puede ser negativo."})

    def save(self, *args, **kwargs):
        self.clean()
        if self.estado_transaccion == 'aprobado' and self.reserva:
            self.reserva.estado = 'confirmada'
            self.reserva.save()
        elif self.estado_transaccion == 'rechazado' and self.reserva and self.reserva.estado == 'pendiente':
            pass # Keep it pending, or maybe cancel? We'll leave as is.
        super().save(*args, **kwargs)

    def nombre_archivo(self):
        """
        Retorna el nombre del archivo de imagen del comprobante.

        Returns:
             str: El nombre base del archivo, o '—' si no hay imagen.
        """
        return os.path.basename(self.imagen_comprobante.name) if self.imagen_comprobante else '—'


class Factura(models.Model):
    """
    Modelo que representa la entidad 'factura' del MER.
    Registra los datos de facturación formal vinculados a una reserva y a su respectivo pago.
    """
    ESTADO_CHOICES = [
        ('emitida', 'Emitida'),
        ('anulada', 'Anulada'),
        ('pagada', 'Pagada'),
    ]

    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Emisión')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='emitida',
        verbose_name='Estado'
    )
    valor_subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor Subtotal'
    )
    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor Total'
    )
    reserva = models.OneToOneField(
        'reservas.Reserva',
        on_delete=models.CASCADE,
        related_name='factura',
        db_column='codigo_reserva',
        verbose_name='Reserva'
    )
    pago = models.ForeignKey(
        Pago,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='facturas',
        db_column='codigo_pago',
        verbose_name='Pago'
    )

    class Meta:
        db_table = 'factura'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

    def __str__(self):
        return f"Factura #{self.pk} — Reserva #{self.reserva.id} — Total: ${self.valor_total}"

