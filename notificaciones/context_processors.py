"""
Context processors para inyectar notificaciones globales en la campanita flotante.
"""

from .models import Auditoria


def lista_notificaciones_global(request):
    if request.user.is_authenticated:
        # Trae las últimas 5 notificaciones/auditorías para la campanita
        alertas = Auditoria.objects.filter(
            codigo_usuario=request.user
        ).order_by('-fecha', '-hora', '-id')[:5]

        # Conteo total de notificaciones del usuario
        contador = Auditoria.objects.filter(
            codigo_usuario=request.user
        ).count()

        return {
            'notificaciones_globales': alertas,
            'contador_notificaciones': contador,
        }

    return {
        'notificaciones_globales': [],
        'contador_notificaciones': 0,
    }