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


    class Meta:
        db_table = 'factura'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

    def __str__(self):
        return f"Factura #{self.pk} — Reserva #{self.reserva.id} — Total: ${self.valor_total}"

