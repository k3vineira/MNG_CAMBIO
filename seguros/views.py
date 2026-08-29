from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PolizaViaje, Aseguradora
from .forms import PolizaForm

def lista_seguros(request):
    """Muestra los planes de seguro disponibles."""
    seguros = Aseguradora.objects.filter(estado=True)
    return render(request, 'seguros/lista_seguros.html', {'seguros': seguros})

@login_required
def adquirir_seguro(request, reserva_id):
    """Permite vincular un seguro a una reserva existente."""
    # Obtenemos la reserva del usuario
    from reservas.models import Reserva
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)

    if request.method == 'POST':
        form = PolizaForm(request.POST)
        if form.is_valid():
            poliza = form.save(commit=False)
            poliza.usuario = request.user
            poliza.reserva = reserva
            # Generar número único de póliza
            import uuid
            poliza.numero_poliza = f"POL-{uuid.uuid4().hex[:8].upper()}"
            poliza.save()
            return redirect('mis_reservas_usuario')
    else:
        form = PolizaForm()

    return render(request, 'seguros/comprar_seguro.html', {'form': form, 'reserva': reserva})
