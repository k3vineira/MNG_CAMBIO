"""
Registro de modelos de la comunidad en el sitio de administración de Django.
"""

from django.contrib import admin
from .models import Calificacion, Blog, PQRS, Comentario,Historial

# Register your models here.
admin.site.register(Calificacion)
admin.site.register(Blog)
admin.site.register(PQRS)
admin.site.register(Comentario)
admin.site.register(Historial)
