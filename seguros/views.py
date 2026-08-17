from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SeguroViaje, Poliza
from .forms import SeguroViajeForm

def lista_seguros(request):
    """Muestra los planes de seguro disponibles."""
    seguros = Poliza.objects.filter(estado=True)
    return render(request, 'seguros/lista_seguros.html', {'seguros': seguros})

@login_required
def adquirir_seguro(request, reserva_id):
    """Permite vincular un seguro a una reserva existente."""
    # Obtenemos la reserva del usuario
    from reservas.models import Reserva
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)

    if request.method == 'POST':
        form = SeguroViajeForm(request.POST)
        if form.is_valid():
            seguro_viaje = form.save(commit=False)
            seguro_viaje.usuario = request.user
            seguro_viaje.reserva = reserva
            # Generar número único de póliza
            import uuid
            seguro_viaje.numero_poliza = f"POL-{uuid.uuid4().hex[:8].upper()}"
            seguro_viaje.save()
            return redirect('mis_reservas_usuario')
    else:
        form = SeguroViajeForm()

    return render(request, 'seguros/comprar_seguro.html', {'form': form, 'reserva': reserva})
