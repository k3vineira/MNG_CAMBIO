"""
Utilidades para el registro de auditoría/notificaciones en el sistema.
"""

from .models import Auditoria


def crear_notificacion_sistema(
    usuario,
    accion=None,
    tabla_afectada="Sistema",
    observacion="",
    valor_anterior="",
    nuevo_valor="",
    titulo=None,
    mensaje=None,
    tipo=None,
):
    """Crea un registro completo en la tabla 'auditoria'.

    Mantiene compatibilidad total con parámetros viejos (titulo, mensaje) y los
    nuevos del MER.
    """
    if usuario and usuario.is_authenticated:
        # Compatibilidad con llamadas viejas si no se usan los nombres del MER
        acciones = accion or titulo or "Acción realizada"
        tabla = tipo.capitalize() if tipo else tabla_afectada
        obs = observacion or mensaje or ""

        return Auditoria.objects.create(
            codigo_usuario=usuario,
            acciones_realizada=acciones,
            tabla_afectada=tabla,
            observacion=obs,
            valor_anterior=valor_anterior,
            nuevo_valor=nuevo_valor,
        )
    return None