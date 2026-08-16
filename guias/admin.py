from django.contrib import admin
from .models import PlanGuia

@admin.register(PlanGuia)
class PlanGuiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'guia', 'paquete', 'idioma_servicio', 'fecha_inicio_plan', 'fecha_fin_plan', 'estado')
    list_filter = ('estado', 'idioma_servicio', 'fecha_inicio_plan')
    search_fields = ('guia__usuario__first_name', 'guia__usuario__last_name', 'paquete__nombre', 'idioma_servicio')
    ordering = ('-fecha_inicio_plan',)
