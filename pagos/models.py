"""
Modelo de datos para los comprobantes de pago enviados por los usuarios.
"""

import os
from django.db import models
from django.conf import settings


class ComprobantePago(models.Model):
    """
    Comprobante de pago subido por un usuario para verificar el pago de una reserva o multa.
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
    reserva = models.ForeignKey(
        'reservas.Reserva',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comprobantes',
        verbose_name='Reserva'
    )

    referencia = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Número de referencia / transacción',
        help_text='Número de comprobante, transacción o referencia bancaria'
    )
    banco_origen = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Banco / medio de pago'
    )
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Monto pagado'
    )
    imagen = models.ImageField(
        upload_to='comprobantes/%Y/%m/',
        verbose_name='Imagen del comprobante'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción / nota adicional'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    nota_admin = models.TextField(
        blank=True,
        verbose_name='Nota del administrador'
    )
    fecha_envio = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de envío')
    fecha_revision = models.DateTimeField(
        null=True, blank=True, verbose_name='Fecha de revisión')

    class Meta:
        verbose_name = 'Comprobante de Pago'
        verbose_name_plural = 'Comprobantes de Pago'
        ordering = ['-fecha_envio']

    def __str__(self):
        """Retorna el ID, usuario y estado del comprobante como representación textual."""
        return f"Comprobante #{self.pk} — {self.usuario.username} — {self.get_estado_display()}"

    def nombre_archivo(self):
        """
        Retorna el nombre del archivo de imagen del comprobante.

        Returns:
            str: El nombre base del archivo, o '—' si no hay imagen.
        """
        return os.path.basename(self.imagen.name) if self.imagen else '—'


class Factura(models.Model):
    """
    Modelo que representa la entidad 'factura' del MER.
    Registra los datos de facturación formal vinculados a una reserva y a su respectivo comprobante de pago.
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
        verbose_name='Valor Subtotal'
    )
    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor Total'
    )
    reserva = models.ForeignKey(
        'reservas.Reserva',
        on_delete=models.CASCADE,
        related_name='facturas',
        db_column='codigo_reserva',
        verbose_name='Reserva'
    )
    pago = models.ForeignKey(
        ComprobantePago,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='facturas',
        db_column='codigo_pago',
        verbose_name='Comprobante de Pago'
    )

    class Meta:
        db_table = 'factura'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

    def __str__(self):
        return f"Factura #{self.pk} — Reserva #{self.reserva.id} — Total: ${self.valor_total}"

