from django.contrib import admin
from .models import PlanGuia

@admin.register(PlanGuia)
class PlanGuiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'guia', 'idioma_servicio', 'fecha_inicio_plan', 'fecha_fin_plan', 'estado')
    list_filter = ('estado', 'idioma_servicio', 'fecha_inicio_plan')
    search_fields = ('guia__first_name', 'guia__last_name', 'idioma_servicio')
    ordering = ('-fecha_inicio_plan',)
