"""
Vistas para la gestión de auditorías servidas como notificaciones al usuario.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Auditoria


@login_required
def marcar_notificacion_leida(request, noti_id):
    """
    Marca un registro de auditoría como leído y redirige al módulo correspondiente.
    """
    noti = get_object_or_404(Auditoria, id=noti_id)
    
    noti.leida = True
    noti.save()

    if hasattr(noti, 'url_destino') and noti.url_destino:
        return redirect(noti.url_destino)

    tipo = noti.tipo.lower() if hasattr(noti, 'tipo') and noti.tipo else ''

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
    Obtiene las auditorías asociadas al usuario y las sirve en la interfaz como Notificaciones.
    """
    notificaciones = Auditoria.objects.filter(
        codigo_usuario=request.user
    ).order_by('-fecha', '-hora')

    return render(
        request,
        'notificaciones.html',
        {'notificaciones': notificaciones},
    )