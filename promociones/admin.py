from django.contrib import admin
from .models import Promocion, PaquetePromocion

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descuento', 'fecha_fin', 'activa')
    list_filter = ('activa', 'fecha_fin')
    search_fields = ('nombre',)

@admin.register(PaquetePromocion)
class PaquetePromocionAdmin(admin.ModelAdmin):
    list_display = ('paquete', 'promocion', 'tarifa')
    list_filter = ('paquete', 'promocion')
    search_fields = ('paquete__nombre', 'promocion__nombre')

