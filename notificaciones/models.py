"""
Modelo de datos para la auditoría del sistema registrada para los usuarios.
"""

from django.conf import settings
from django.db import models


class Auditoria(models.Model):
    """
    Registro de auditoría del sistema sobre acciones realizadas por los usuarios.
    """
    acciones_realizada = models.CharField(max_length=255)
    tabla_afectada = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)
    valor_anterior = models.TextField(blank=True, null=True)
    nuevo_valor = models.TextField(blank=True, null=True)
    codigo_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auditorias',
    )

    class Meta:
        ordering = ['-fecha', '-hora']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f'{self.acciones_realizada} - {self.codigo_usuario.username}'