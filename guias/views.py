from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.decoradores import requiere_administrador
from .models import PlanGuia
from .forms import PlanGuiaForm

@requiere_administrador
def listar_planes_guia(request):
    planes = PlanGuia.objects.all().select_related('guia', 'guia__usuario', 'paquete').order_by('-fecha_creacion')
    return render(request, 'guias/listar_planes.html', {'planes': planes, 'titulo': 'Asignación de Guías'})

@requiere_administrador
def crear_plan_guia(request):
    if request.method == 'POST':
        form = PlanGuiaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignación creada exitosamente.')
            return redirect('listar_planes_guia')
        else:
            messages.error(request, 'Error al crear la asignación. Revisa los datos ingresados.')
    else:
        form = PlanGuiaForm()
    return render(request, 'guias/formulario_plan.html', {'form': form, 'titulo': 'Nueva Asignación de Guía'})

@requiere_administrador
def editar_plan_guia(request, pk):
    plan = get_object_or_404(PlanGuia, pk=pk)
    if request.method == 'POST':
        form = PlanGuiaForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignación actualizada exitosamente.')
            return redirect('listar_planes_guia')
        else:
            messages.error(request, 'Error al actualizar la asignación. Revisa los datos ingresados.')
    else:
        form = PlanGuiaForm(instance=plan)
    return render(request, 'guias/formulario_plan.html', {'form': form, 'titulo': 'Editar Asignación de Guía', 'plan': plan})

@requiere_administrador
def eliminar_plan_guia(request, pk):
    plan = get_object_or_404(PlanGuia, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Asignación eliminada exitosamente.')
    return redirect('listar_planes_guia')
