"""
Vistas para la gestión de comprobantes de pago integrados directamente en Reserva.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from reservas.models import Reserva, Cancelacion
from django.db.models import Q, OuterRef, Subquery, Sum
from core.decoradores import requiere_autenticacion, requiere_administrador
from decimal import Decimal


@requiere_autenticacion
def enviar_comprobante(request):
    """Usuario sube un comprobante de pago vinculado a una reserva."""
    penalidad_subquery = Cancelacion.objects.filter(
        reserva=OuterRef('pk'),
        estado='aceptada'
    ).values('penalidad')[:1]

    reservas_usuario = Reserva.objects.filter(usuario=request.user).filter(
        Q(estado='pendiente') |
        Q(estado='cancelada', cancelaciones__estado='aceptada',
          cancelaciones__penalidad__gt=0)
    ).annotate(
        multa=Subquery(penalidad_subquery)
    ).distinct()

    # Excluir reservas que ya tengan comprobantes en proceso para evitar duplicidad
    reservas_usuario = reservas_usuario.exclude(estado_pago__in=['aprobado', 'pendiente'])

    if request.method == 'POST':
        reserva_id = request.POST.get('reserva')
        if not reserva_id:
            messages.error(request, 'Debe seleccionar una reserva válida.')
            return redirect('enviar_comprobante')
            
        reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
        
        # Manually updating fields instead of form since Pago model is gone
        reserva.referencia_pago = request.POST.get('referencia', '')
        reserva.banco_origen_pago = request.POST.get('banco_origen', '')
        try:
            reserva.monto_pagado = Decimal(request.POST.get('monto', '0'))
        except:
            reserva.monto_pagado = Decimal('0.00')
            
        if 'imagen_comprobante' in request.FILES:
            reserva.imagen_comprobante = request.FILES['imagen_comprobante']
            
        reserva.estado_pago = 'pendiente'
        reserva.fecha_envio_pago = timezone.now()
        reserva.save()
        
        messages.success(request, '¡Comprobante enviado! Será revisado por el equipo en breve.')
        return redirect('mis_comprobantes')

    else:
        # Pass the queryset to template to show dropdown
        selected_reserva_id = request.GET.get('reserva_id')

    comprobantes = Reserva.objects.filter(usuario=request.user).exclude(estado_pago='sin_pago').order_by('-fecha_envio_pago')
    
    total_pendientes = comprobantes.filter(estado_pago='pendiente').count()
    total_aprobados = comprobantes.filter(estado_pago='aprobado').aggregate(t=Sum('monto_pagado'))['t'] or Decimal('0.00')
    total_rechazados = comprobantes.filter(estado_pago='rechazado').count()

    context = {
        'reservas_elegibles': reservas_usuario,
        'selected_reserva_id': selected_reserva_id,
        'comprobantes': comprobantes,
        'total_pendientes': total_pendientes,
        'total_aprobados': total_aprobados,
        'total_rechazados': total_rechazados,
    }
    return render(request, 'pagos/enviar_comprobante.html', context)


@requiere_autenticacion
def mis_comprobantes(request):
    """Usuario ve el historial de sus comprobantes optimizado."""
    comprobantes = Reserva.objects.filter(usuario=request.user).exclude(estado_pago='sin_pago')\
        .select_related('paquete')\
        .order_by('-fecha_envio_pago')
        
    monto_aprobado = comprobantes.filter(estado_pago='aprobado').aggregate(t=Sum('monto_pagado'))['t'] or Decimal('0.00')

    context = {
        'comprobantes':     comprobantes,
        'total_pendientes': comprobantes.filter(estado_pago='pendiente').count(),
        'total_aprobados':  monto_aprobado,
        'total_rechazados': comprobantes.filter(estado_pago='rechazado').count(),
    }
    return render(request, 'pagos/mis_comprobantes.html', context)


@requiere_administrador
def admin_comprobantes(request):
    """Admin ve todos los comprobantes con filtros por estado."""
    estado_filtro = request.GET.get('estado', '')
    comprobantes = Reserva.objects.exclude(estado_pago='sin_pago').select_related('usuario', 'paquete').order_by('-fecha_envio_pago')

    if estado_filtro:
        comprobantes = comprobantes.filter(estado_pago=estado_filtro)
    else:
        comprobantes = comprobantes.exclude(estado_pago='rechazado')

    total = Reserva.objects.exclude(estado_pago='sin_pago').count()
    total_pendientes = Reserva.objects.filter(estado_pago='pendiente').count()
    total_aprobados = Reserva.objects.filter(estado_pago='aprobado').aggregate(t=Sum('monto_pagado'))['t'] or Decimal('0.00')
    total_rechazados = Reserva.objects.filter(estado_pago='rechazado').count()

    context = {
        'comprobantes':     comprobantes,
        'estado_filtro':    estado_filtro,
        'total':            total,
        'total_pendientes': total_pendientes,
        'total_aprobados':  total_aprobados,
        'total_rechazados': total_rechazados,
    }
    return render(request, 'pagos/admin_comprobantes.html', context)


@requiere_administrador
def admin_revisar_comprobante(request, pk):
    """Admin aprueba, rechaza o deja pendiente un comprobante integrado."""
    comprobante = get_object_or_404(Reserva, pk=pk)

    if request.method == 'POST':
        if comprobante.estado_pago in ('aprobado', 'rechazado'):
            messages.error(request, 'Este comprobante ya ha sido procesado y no puede modificarse.')
            return redirect('admin_comprobantes')

        nuevo_estado = request.POST.get('estado_pago')
        nota_admin = request.POST.get('nota_admin_pago', '')
        
        comprobante.estado_pago = nuevo_estado
        comprobante.nota_admin_pago = nota_admin
        
        if nuevo_estado == 'aprobado':
            if comprobante.estado != 'cancelada':
                comprobante.estado = 'confirmada'
                
                comprobante.save()
                from core.utils import enviar_correo_confirmacion_con_factura
                try:
                    enviar_correo_confirmacion_con_factura(comprobante, request=request)
                except Exception as e:
                    print(f"Error enviando correo de pago exitoso con factura: {e}")

                messages.success(request, f'Comprobante #{pk} APROBADO. La Reserva #{comprobante.id} ha sido confirmada y se ha notificado al cliente.')
                return redirect('admin_comprobantes')
            else:
                comprobante.save()
                messages.success(request, f'Comprobante #{pk} APROBADO para el pago de la multa de la Reserva #{comprobante.id}.')
        elif nuevo_estado == 'rechazado':
            comprobante.save()
            messages.warning(request, f'Comprobante #{pk} marcado como RECHAZADO.')
        else:
            comprobante.save()
            messages.success(request, f'Comprobante #{pk} marcado como Pendiente.')
            
        return redirect('admin_comprobantes')

    context = {'comprobante': comprobante}
    return render(request, 'pagos/admin_revisar_comprobante.html', context)


@requiere_administrador
def admin_eliminar_comprobante(request, pk):
    """Admin elimina/resetea los datos de pago de una reserva."""
    if request.method == 'POST':
        res = get_object_or_404(Reserva, id=pk)
        res.referencia_pago = ''
        res.banco_origen_pago = ''
        res.monto_pagado = 0
        if res.imagen_comprobante:
            res.imagen_comprobante.delete()
        res.estado_pago = 'sin_pago'
        res.nota_admin_pago = ''
        res.save()
        messages.success(request, f'Datos de pago de la reserva #{pk} eliminados correctamente.')
    return redirect('admin_comprobantes')


@requiere_autenticacion
def mis_rechazos(request):
    """Muestra al usuario autenticado sus pagos rechazados y cancelaciones rechazadas."""
    if request.user.is_staff:
        return redirect('dashboard')

    pagos_rechazados = Reserva.objects.filter(
        usuario=request.user,
        estado_pago='rechazado'
    ).select_related('paquete').order_by('-fecha_envio_pago')

    cancelaciones_rechazadas = Cancelacion.objects.filter(
        reserva__usuario=request.user,
        estado='rechazada'
    ).select_related('reserva__paquete').order_by('-id')

    context = {
        'pagos_rechazados': pagos_rechazados,
        'cancelaciones_rechazadas': cancelaciones_rechazadas,
        'total_pagos_rechazados': pagos_rechazados.count(),
        'total_cancelaciones_rechazadas': cancelaciones_rechazadas.count(),
    }
    return render(request, 'private/rechazos.html', context)
