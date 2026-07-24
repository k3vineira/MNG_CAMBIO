"""
Context processors para inyectar notificaciones globales en todos los templates.
"""

from .models import Notificacion
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

def lista_notificaciones_global(request):
    """
    Context processor optimizado que provee las notificaciones del usuario a todos los templates.
    """
    if request.user.is_authenticated:
        storage = messages.get_messages(request)
        messages_list = list(storage)
        storage.used = False
        
        if messages_list:
            recent_limit = timezone.now() - timedelta(seconds=5)
            for msg in messages_list:
                tag = msg.tags or ''
                if 'success' in tag:
                    titulo = "¡Excelente!"
                elif 'error' in tag or 'danger' in tag:
                    titulo = "¡Error!"
                elif 'warning' in tag:
                    titulo = "¡Atención!"
                else:
                    titulo = "Información"
                    
                texto_mensaje = str(msg.message)
                texto_lower = texto_mensaje.lower()
                if any(k in texto_lower for k in ['reserva', 'pago', 'comprobante', 'factura']):
                    tipo = 'reserva'
                elif any(k in texto_lower for k in ['pqrs', 'solicitud', 'reclamo', 'cancelación']):
                    tipo = 'pqrs'
                else:
                    tipo = 'sistema'
                    
                if not Notificacion.objects.filter(
                    cliente=request.user,
                    titulo=titulo,
                    mensaje=texto_mensaje,
                    tipo=tipo,
                    fecha_creacion__gte=recent_limit
                ).exists():
                    Notificacion.objects.create(
                        cliente=request.user,
                        titulo=titulo,
                        mensaje=texto_mensaje,
                        tipo=tipo
                    )

        qs = Notificacion.objects.filter(cliente=request.user)
        alertas = list(qs.order_by('-id')[:5])
        contador = sum(1 for n in alertas if not n.leida) if len(alertas) < 5 else qs.filter(leida=False).count()
        
        return {
            'notificaciones_globales': alertas,
            'contador_notificaciones': contador
        }
    return {
        'notificaciones_globales': [],
        'contador_notificaciones': 0
    }