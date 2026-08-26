from django.contrib import admin
from .models import Promocion

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descuento', 'fecha_fin', 'activa')
    list_filter = ('activa', 'fecha_fin')
    search_fields = ('nombre',)
