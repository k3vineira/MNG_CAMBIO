"""
Vistas para la gestión de notificaciones de usuario.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notificacion

@login_required
def marcar_notificacion_leida(request, noti_id):
    """
    Marca una notificación como leída y redirige al módulo o vista exacta.
    """
   
    noti = get_object_or_404(Notificacion, id=noti_id)
    
    noti.leida = True
    noti.save()

    if hasattr(noti, 'url_destino') and noti.url_destino:
        return redirect(noti.url_destino)

   
    tipo = noti.tipo.lower() if noti.tipo else ''


    if tipo in ['paquete', 'nuevo_paquete']:
        return redirect('listar_paquetes')  
    elif tipo == 'categoria':
        return redirect('listar_categorias')
    elif tipo == 'temporada':
        return redirect('listar_temporadas')
    elif tipo == 'actividad':
        return redirect('listar_actividades')
    elif tipo == 'tarifa':
        return redirect('listar_tarifas')


    elif tipo in ['reserva', 'crear_reserva', 'editar_reserva', 'eliminar_reserva']:
     
        if request.user.is_staff or request.user.is_superuser:
            return redirect('listar_reservas')
        return redirect('mis_reservas_usuario')
        
    elif tipo in ['pago', 'comprobante']:
        return redirect('admin_comprobantes')
    elif tipo == 'pago_rechazado':
        return redirect('admin_pagos_rechazados')
    elif tipo == 'cancelacion':
        return redirect('admin_cancelaciones')

   
    elif tipo == 'usuario':
        return redirect('gestion_usuarios')
    elif tipo == 'guia':
        return redirect('gestion_guias')

   
    elif tipo == 'pqrs':
        if request.user.is_staff or request.user.is_superuser:
            return redirect('listar_pqrs')
        return redirect('mis_pqrs')
    elif tipo == 'comentario':
        return redirect('admin_comentarios')

    elif tipo in ['contenido', 'banner', 'anuncio']:
        return redirect('gestion_contenido')

    if request.user.is_staff or request.user.is_superuser:
        return redirect('dashboard') 
    
    return redirect('dashboard_turista')

@login_required
def lista_notificaciones(request):
    """
    Muestra el historial completo de notificaciones del usuario autenticado.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Página con la lista de notificaciones del usuario.
    """
    notificaciones = Notificacion.objects.filter(cliente=request.user).order_by('-id')
    return render(request, 'historial_completo.html', {
        'notificaciones': notificaciones
    })