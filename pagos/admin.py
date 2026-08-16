from django.contrib import admin
from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'reserva', 'referencia',
                    'banco_origen', 'monto', 'estado', 'fecha_envio', 'fecha_pago')
    list_filter = ('estado', 'banco_origen', 'fecha_envio')
    search_fields = ('usuario__username', 'usuario__email',
                     'referencia', 'banco_origen')
    ordering = ('-fecha_envio',)

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            # If the payment is already processed (aprobado/rechazado), EVERYTHING is readonly
            if obj.estado in ['aprobado', 'rechazado']:
                return [f.name for f in self.model._meta.fields]
            # If pending, we lock the user-submitted fields to prevent tampering,
            # but allow admin to change 'estado' and 'nota_admin'.
            return ('usuario', 'reserva', 'referencia', 'banco_origen', 'monto', 'imagen', 'descripcion', 'fecha_pago', 'fecha_envio', 'fecha_revision')
        # If adding a new object (though typically done via frontend)
        return ('fecha_envio', 'fecha_revision')

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of processed payments
        if obj and obj.estado in ['aprobado', 'rechazado']:
            return False
        return super().has_delete_permission(request, obj)
