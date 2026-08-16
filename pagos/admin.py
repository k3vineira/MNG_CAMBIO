from django.contrib import admin
from .models import ComprobantePago, Factura


@admin.register(ComprobantePago)
class ComprobantePagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'reserva', 'referencia',
                    'banco_origen', 'monto', 'estado', 'fecha_envio')
    list_filter = ('estado', 'banco_origen', 'fecha_envio')
    search_fields = ('usuario__username', 'usuario__email',
                     'referencia', 'banco_origen')
    readonly_fields = ('fecha_envio',)
    ordering = ('-fecha_envio',)


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'fecha_emision', 'valor_subtotal', 'valor_total', 'estado', 'pago')
    list_filter = ('estado', 'fecha_emision')
    search_fields = ('reserva__id', 'reserva__usuario__username', 'pago__referencia')
    readonly_fields = ('fecha_emision',)
    ordering = ('-fecha_emision',)

