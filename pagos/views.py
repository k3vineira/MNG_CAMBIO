"""
Vistas para la gestión de comprobantes de pago: envío, revisión y administración por parte del staff.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Pago
from reservas.models import Reserva, Cancelacion
from django.db.models import Q, OuterRef, Subquery
from core.decoradores import requiere_autenticacion, requiere_administrador
from .forms import PagoForm, RevisarComprobanteForm


@requiere_autenticacion
def enviar_comprobante(request):
    """Usuario sube un comprobante de pago vinculado a una reserva o multa."""
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

    # Excluir reservas que ya tengan comprobantes en proceso para evitar duplicidad real
    reservas_usuario = reservas_usuario.exclude(pago__estado_transaccion__in=['aprobado', 'pendiente'])

    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES, reservas=reservas_usuario)
        if form.is_valid():
            comprobante = form.save(commit=False)
            comprobante.usuario = request.user
            
            # The form already validates that the reserva is within the queryset (reservas_usuario)
            comprobante.save()
            messages.success(request, '¡Comprobante enviado! Será revisado por el equipo en breve.')
            return redirect('mis_comprobantes')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario y completa todos los campos obligatorios.')

    else:
        form = PagoForm(reservas=reservas_usuario)
        # Select initial reservation if passed via GET parameter
        selected_reserva_id = request.GET.get('reserva_id')
        if selected_reserva_id:
            form.initial['reserva'] = selected_reserva_id

    comprobantes = Pago.objects.filter(usuario=request.user)
    context = {
        'form':               form,
        'comprobantes':       comprobantes,
        'total_pendientes':   comprobantes.filter(estado_transaccion='pendiente').count(),
        'total_aprobados':    sum(p.monto or (p.reserva.monto_total if p.reserva else 0) for p in comprobantes.filter(estado_transaccion='aprobado').select_related('reserva')),
        'total_rechazados':   comprobantes.filter(estado_transaccion='rechazado').count(),
    }
    return render(request, 'pagos/enviar_comprobante.html', context)


@requiere_autenticacion
def mis_comprobantes(request):
    """Usuario ve el historial de sus comprobantes optimizado."""
    from django.db.models import Sum, DecimalField
    from django.db.models.functions import Coalesce, Cast

    comprobantes = Pago.objects.filter(usuario=request.user)\
        .select_related('reserva', 'reserva__paquete')\
        .order_by('-fecha_envio')
        
    monto_aprobado = comprobantes.filter(estado_transaccion='aprobado').aggregate(
        total=Sum(Coalesce(
            'monto',
            Cast('reserva__monto_total', DecimalField(max_digits=12, decimal_places=2)),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        ))
    )['total'] or 0

    context = {
        'comprobantes':     comprobantes,
        'total_pendientes': comprobantes.filter(estado_transaccion='pendiente').count(),
        'total_aprobados':  monto_aprobado,
        'total_rechazados': comprobantes.filter(estado_transaccion='rechazado').count(),
    }
    return render(request, 'pagos/mis_comprobantes.html', context)


@requiere_administrador
def admin_comprobantes(request):
    """Admin ve todos los comprobantes con filtros por estado."""
    estado_filtro = request.GET.get('estado', '')
    comprobantes = Pago.objects.select_related(
        'usuario', 'reserva').all()

    if estado_filtro:
        comprobantes = comprobantes.filter(estado_transaccion=estado_filtro)
    else:
        # Excluir rechazados de la vista general
        comprobantes = comprobantes.exclude(estado_transaccion='rechazado')

    total = Pago.objects.count()
    total_pendientes = Pago.objects.filter(
        estado_transaccion='pendiente').count()
    total_aprobados = sum(p.monto or (p.reserva.monto_total if p.reserva else 0) for p in Pago.objects.filter(estado_transaccion='aprobado').select_related('reserva'))
    total_rechazados = Pago.objects.filter(
        estado_transaccion='rechazado').count()

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
    """Admin aprueba, rechaza o deja pendiente un comprobante."""
    from django.core.exceptions import ValidationError
    comprobante = get_object_or_404(Pago, pk=pk)

    if request.method == 'POST':
        if comprobante.estado_transaccion in ('aprobado', 'rechazado'):
            messages.error(request, 'Este comprobante ya ha sido procesado y no puede modificarse.')
            return redirect('admin_comprobantes')

        form = RevisarComprobanteForm(request.POST, instance=comprobante)
        if form.is_valid():
            # Actualizamos el objeto comprobante con los datos limpios del formulario
            nuevo_estado = form.cleaned_data.get('estado_transaccion')
            comprobante.fecha_revision = timezone.now()
            
            try:
                # El método save() del modelo Pago ejecuta self.clean(), el cual valida el estado
                comprobante.save()
            except ValidationError as e:
                # Si falla la validación del modelo, inyectamos los errores en el formulario
                if hasattr(e, 'message_dict'):
                    for field, errors in e.message_dict.items():
                        for err in errors:
                            # Map model fields to form fields if they match
                            form.add_error(field if field in form.fields else None, err)
                else:
                    for err in e.messages:
                        form.add_error(None, err)
                
                # Volvemos a renderizar la plantilla con el formulario que contiene los errores y los datos introducidos
                context = {'comprobante': comprobante, 'form': form}
                return render(request, 'pagos/admin_revisar_comprobante.html', context)

            # --- SI SE APRUEBA LA TRANSACCIÓN (Y SE GUARDÓ CON ÉXITO) ---
            if nuevo_estado == 'aprobado' and comprobante.reserva:
                if comprobante.reserva.estado != 'cancelada':
                    comprobante.reserva.estado = 'confirmada'
                    comprobante.reserva.save()
                    
                    # Enviar correo de éxito con la factura en PDF adjunta (encriptada) y nuevo diseño tipo OTP
                    from core.utils import enviar_correo_confirmacion_con_factura
                    try:
                        enviar_correo_confirmacion_con_factura(comprobante.reserva, request=request)
                    except Exception as e:
                        print(f"Error enviando correo de pago exitoso con factura: {e}")

                    messages.success(
                        request,
                        f'Comprobante #{pk} APROBADO. La Reserva #{comprobante.reserva.id} ha sido confirmada y se ha notificado al cliente.'
                    )
                    return redirect('admin_comprobantes')
                else:
                    messages.success(
                        request,
                        f'Comprobante #{pk} APROBADO para el pago de la multa de la Reserva #{comprobante.reserva.id}.'
                    )
            elif nuevo_estado == 'rechazado':
                messages.warning(
                    request,
                    f'Comprobante #{pk} marcado como RECHAZADO.'
                )
            else:
                messages.success(
                    request,
                    f'Comprobante #{pk} marcado como {comprobante.get_estado_transaccion_display()}.'
                )
            return redirect('admin_comprobantes')

    else:
        # En solicitudes GET, instanciamos el formulario con los datos actuales
        form = RevisarComprobanteForm(instance=comprobante)

    context = {'comprobante': comprobante, 'form': form}
    return render(request, 'pagos/admin_revisar_comprobante.html', context)


@requiere_administrador
def admin_eliminar_comprobante(request, pk):
    """Admin elimina un comprobante."""
    if request.method == 'POST':
        comp = get_object_or_404(Pago, id=pk)
        comp.delete()
        messages.success(request, f'Comprobante #{pk} eliminado correctamente.')
    return redirect('admin_comprobantes')

    # PÁGINA DE PAGOS RECHAZADOS Y CANCELACIONES RECHAZADAS


@requiere_autenticacion
def mis_rechazos(request):
    """
    Muestra al usuario autenticado sus pagos rechazados y cancelaciones rechazadas.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Página con los comprobantes y cancelaciones rechazadas del usuario.
    """
    if request.user.is_staff:
        return redirect('dashboard')

    try:
        from pagos.models import Pago
        pagos_rechazados = Pago.objects.filter(
            usuario=request.user,
            estado_transaccion='rechazado'
        ).select_related('reserva__paquete').order_by('-fecha_revision')
    except ImportError:
        pagos_rechazados = []

    try:
        from reservas.models import Cancelacion
        cancelaciones_rechazadas = Cancelacion.objects.filter(
            reserva__usuario=request.user,
            estado='rechazada'
        ).select_related('reserva__paquete').order_by('-id')
    except ImportError:
        cancelaciones_rechazadas = []

    total_pagos_rechazados = len(pagos_rechazados) if isinstance(pagos_rechazados, list) else pagos_rechazados.count()
    total_cancelaciones_rechazadas = len(cancelaciones_rechazadas) if isinstance(cancelaciones_rechazadas, list) else cancelaciones_rechazadas.count()

    context = {
        'pagos_rechazados': pagos_rechazados,
        'cancelaciones_rechazadas': cancelaciones_rechazadas,
        'total_pagos_rechazados': total_pagos_rechazados,
        'total_cancelaciones_rechazadas': total_cancelaciones_rechazadas,
    }

    return render(request, 'private/rechazos.html', context)
