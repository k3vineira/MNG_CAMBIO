from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms
from django.db.models import Count, Q
from .models import Paquete, Actividades, Categoria, Tarifa, Temporada
from .forms import PaqueteForm,CategoriaForm, ActividadesForm, TarifaForm, TemporadaForm
from auditoria.utils import crear_notificacion_sistema



# ==========================================
# MIXINS DE VALIDACIÓN Y PERMISOS
# ==========================================

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para asegurar que solo usuarios autenticados con permisos
    de staff/administrador puedan acceder a las vistas administrativas.
    """
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff


# ==========================================
# VISTAS PÚBLICAS
# ==========================================

def destinos(request):
    """
    Vista pública que filtra y devuelve la lista de paquetes turísticos disponibles.
    Incluye validaciones y sanitización para los parámetros GET.
    """
    destinos_list = Paquete.objects.filter(estado=True)
    destinos_sugerencias = Paquete.objects.filter(estado=True).values('nombre').distinct()

    # Validar y sanitizar búsqueda textual
    busqueda = request.GET.get('q', '').strip()
    if busqueda and len(busqueda) <= 100:
        destinos_list = destinos_list.filter(nombre__icontains=busqueda)

    # Validar que precio_max sea un decimal/entero positivo válido
    precio_max = request.GET.get('precio_max', '').strip()
    if precio_max:
        try:
            precio_decimal = Decimal(precio_max)
            if precio_decimal >= 0:
                destinos_list = destinos_list.filter(
                    tarifas__precio_adulto__lte=precio_decimal
                ).distinct()
        except (InvalidOperation, TypeError):
            pass  # Ignorar filtro si envían un valor no numérico o malicioso

    # Validar parámetro estricto de apto_menores
    apto_menores = request.GET.get('apto_menores', '').strip().lower()
    if apto_menores == 'si':
        destinos_list = destinos_list.exclude(actividades__apto_para_menores=False).distinct()
    elif apto_menores == 'no':
        destinos_list = destinos_list.exclude(actividades__apto_para_menores=True).distinct()

    # Validar que categoria_id sea un entero válido
    categoria_id = request.GET.get('categoria', '').strip()
    if categoria_id:
        try:
            cat_id = int(categoria_id)
            if cat_id > 0:
                destinos_list = destinos_list.filter(categoria_id=cat_id)
        except (ValueError, TypeError):
            pass

    # Carga optimizada
    destinos_list = destinos_list.select_related('categoria').prefetch_related('actividades', 'tarifas__temporada')
    categorias_list = Categoria.objects.filter(estado=True)

    context = {
        'destinos': destinos_list,
        'destinos_sugerencias': destinos_sugerencias,
        'categorias': categorias_list
    }
    return render(request, 'usuario/destinos.html', context)


def reservas(request):
    context = {'reservas': []}
    return render(request, 'usuario/reservas.html', context)


# ==========================================
# PAQUETES
# ==========================================

class PaqueteListView(StaffRequiredMixin, ListView):
    model = Paquete
    template_name = 'admin/paquetes/paquetes.html'
    context_object_name = 'paquetes'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('categoria').prefetch_related('actividades', 'tarifas')
        categoria_id = self.request.GET.get('categoria', '').strip()
        if categoria_id:
            try:
                cat_id = int(categoria_id)
                if cat_id > 0:
                    queryset = queryset.filter(categoria_id=cat_id)
            except (ValueError, TypeError):
                pass
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Paquete.objects.aggregate(
            total=Count('id'),
            activos=Count('id', filter=Q(estado=True)),
            inactivos=Count('id', filter=Q(estado=False))
        )
        context.update(stats)
        context['stats_list'] = [
            ('Total Paquetes', stats['total'], 'text-dark'),
            ('Activos', stats['activos'], 'text-success'),
            ('Inactivos', stats['inactivos'], 'text-danger'),
        ]
        context['categorias'] = Categoria.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('categoria', '')
        return context


class PaqueteCreateView(StaffRequiredMixin, CreateView):
    model = Paquete
    form_class = PaqueteForm
    template_name = 'admin/paquetes/agregar_paquete.html'
    success_url = reverse_lazy('listar_paquetes')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="NUEVO PAQUETE CREADO",
            tabla_afectada="Paquetes",
            observacion=f"Se ha creado con éxito el paquete turístico: '{self.object.nombre}'.",
            valor_anterior="Ninguno (Registro Nuevo)",
            nuevo_valor=f"Nombre: {self.object.nombre}, Categoría: {self.object.categoria}"
        )
        return response


class PaqueteUpdateView(StaffRequiredMixin, UpdateView):
    model = Paquete
    form_class = PaqueteForm
    template_name = 'admin/paquetes/editar_paquete.html'
    success_url = reverse_lazy('listar_paquetes')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        paquete_antiguo = self.get_object()
        valor_viejo = f"Nombre: {paquete_antiguo.nombre}, Categoría: {paquete_antiguo.categoria}, Estado: {'Activo' if paquete_antiguo.estado else 'Inactivo'}"

        response = super().form_valid(form)

        valor_nuevo = f"Nombre: {self.object.nombre}, Categoría: {self.object.categoria}, Estado: {'Activo' if self.object.estado else 'Inactivo'}"

        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="PAQUETE MODIFICADO",
            tabla_afectada="Paquetes",
            observacion=f"El paquete '{self.object.nombre}' ha sido modificado correctamente.",
            valor_anterior=valor_viejo,
            nuevo_valor=valor_nuevo
        )
        return response


class PaqueteDeleteView(StaffRequiredMixin, DeleteView):
    model = Paquete
    template_name = 'admin/paquetes/eliminar_paquete.html'
    success_url = reverse_lazy('listar_paquetes')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Validar integridad referencial: Prevenir borrado si el paquete tiene tarifas asociadas
        if self.object.tarifas.exists():
            messages.error(request, f"No se puede eliminar el paquete '{self.object.nombre}' porque tiene tarifas registradas.")
            return render(request, self.template_name, {'object': self.object})

        nombre_paquete = self.object.nombre
        valor_viejo = f"ID: {self.object.id}, Nombre: {self.object.nombre}, Categoría: {self.object.categoria}"
        
        response = super().delete(request, *args, **kwargs)

        crear_notificacion_sistema(
            usuario=request.user,
            accion="PAQUETE ELIMINADO",
            tabla_afectada="Paquetes",
            observacion=f"Se ha eliminado del sistema el paquete: '{nombre_paquete}'.",
            valor_anterior=valor_viejo,
            nuevo_valor="Registro Eliminado"
        )
        return response


# ==========================================
# ACTIVIDADES
# ==========================================

class ActividadesListView(StaffRequiredMixin, ListView):
    model = Actividades
    template_name = 'admin/actividades/actividades.html'
    context_object_name = 'actividades'

    def get_queryset(self):
        queryset = super().get_queryset()
        apto_menores_param = self.request.GET.get('apto_menores', '').strip().lower()
        if apto_menores_param == 'si':
            queryset = queryset.filter(apto_para_menores=True)
        elif apto_menores_param == 'no':
            queryset = queryset.filter(apto_para_menores=False)
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Actividades.objects.aggregate(
            total=Count('id'),
            activas=Count('id', filter=Q(estado=True)),
            inactivas=Count('id', filter=Q(estado=False))
        )
        context.update(stats)
        context['stats_list'] = [
            ('Total Actividades', stats['total'], 'text-dark'),
            ('Activas', stats['activas'], 'text-success'),
            ('Inactivas', stats['inactivas'], 'text-danger'),
        ]
        context['apto_menores_seleccionado'] = self.request.GET.get('apto_menores', '')
        return context


class ActividadesCreateView(StaffRequiredMixin, CreateView):
    model = Actividades
    form_class = ActividadesForm
    template_name = 'admin/actividades/agregar_actividad.html'
    success_url = reverse_lazy('listar_actividades')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="NUEVA ACTIVIDAD CREADA",
            tabla_afectada="Actividades",
            observacion=f"Se ha registrado con éxito la actividad: '{self.object.nombre}'.",
            valor_anterior="Ninguno (Registro Nuevo)",
            nuevo_valor=f"Nombre: {self.object.nombre}, Dificultad: {self.object.nivel_dificultad}"
        )
        return response


class ActividadesUpdateView(StaffRequiredMixin, UpdateView):
    model = Actividades
    form_class = ActividadesForm
    template_name = 'admin/actividades/editar_actividad.html'
    success_url = reverse_lazy('listar_actividades')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        actividad_antigua = self.get_object()
        valor_viejo = f"Nombre: {actividad_antigua.nombre}, Dificultad: {actividad_antigua.nivel_dificultad}, Estado: {'Activa' if actividad_antigua.estado else 'Inactiva'}"

        response = super().form_valid(form)

        valor_nuevo = f"Nombre: {self.object.nombre}, Dificultad: {self.object.nivel_dificultad}, Estado: {'Activa' if self.object.estado else 'Inactiva'}"

        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="ACTIVIDAD MODIFICADA",
            tabla_afectada="Actividades",
            observacion=f"La actividad '{self.object.nombre}' ha sido actualizada correctamente.",
            valor_anterior=valor_viejo,
            nuevo_valor=valor_nuevo
        )
        return response


class ActividadesDeleteView(StaffRequiredMixin, DeleteView):
    model = Actividades
    template_name = 'admin/actividades/eliminar_actividad.html'
    success_url = reverse_lazy('listar_actividades')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Validar integridad: Prevenir eliminación si pertenece a paquetes activos
        if self.object.paquete_set.exists():
            messages.error(request, f"No se puede eliminar la actividad '{self.object.nombre}' porque está vinculada a uno o más paquetes.")
            return render(request, self.template_name, {'object': self.object})

        nombre_actividad = self.object.nombre
        valor_viejo = f"ID: {self.object.id}, Nombre: {self.object.nombre}, Dificultad: {self.object.nivel_dificultad}"

        response = super().delete(request, *args, **kwargs)

        crear_notificacion_sistema(
            usuario=request.user,
            accion="ACTIVIDAD ELIMINADA",
            tabla_afectada="Actividades",
            observacion=f"Se ha quitado del sistema la actividad: '{nombre_actividad}'.",
            valor_anterior=valor_viejo,
            nuevo_valor="Registro Eliminado"
        )
        return response


# ==========================================
# CATEGORÍAS
# ==========================================

class CategoriaListView(StaffRequiredMixin, ListView):
    model = Categoria
    template_name = 'admin/categorias/categorias.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Categoria.objects.aggregate(
            total=Count('id'),
            activas=Count('id', filter=Q(estado=True)),
            inactivas=Count('id', filter=Q(estado=False))
        )
        context['stats_list'] = [
            ('Total Categorías', stats['total'], 'text-dark'),
            ('Activas', stats['activas'], 'text-success'),
            ('Inactivas', stats['inactivas'], 'text-danger'),
        ]
        return context


class CategoriaCreateView(StaffRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'admin/categorias/agregar_categoria.html'
    success_url = reverse_lazy('listar_categorias')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="NUEVA CATEGORIA CREADA",
            tabla_afectada="Categorías",
            observacion=f"Se ha registrado con éxito la categoría: '{self.object.nombre}'.",
            valor_anterior="Ninguno (Registro Nuevo)",
            nuevo_valor=f"Nombre: {self.object.nombre}"
        )
        return response


class CategoriaUpdateView(StaffRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'admin/categorias/editar_categoria.html'
    success_url = reverse_lazy('listar_categorias')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        cat_antigua = self.get_object()
        valor_viejo = f"Nombre: {cat_antigua.nombre}, Descripción: {cat_antigua.descripcion}"

        response = super().form_valid(form)

        valor_nuevo = f"Nombre: {self.object.nombre}, Descripción: {self.object.descripcion}"

        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="CATEGORIA MODIFICADA",
            tabla_afectada="Categorías",
            observacion=f"La categoría '{self.object.nombre}' ha sido actualizada correctamente.",
            valor_anterior=valor_viejo,
            nuevo_valor=valor_nuevo
        )
        return response


class CategoriaDeleteView(StaffRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'admin/categorias/eliminar_categoria.html'
    success_url = reverse_lazy('listar_categorias')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Validar integridad: No eliminar categoría si está asignada a algún paquete
        if self.object.paquete_set.exists():
            messages.error(request, f"No se puede eliminar la categoría '{self.object.nombre}' porque contiene paquetes asociados.")
            return render(request, self.template_name, {'object': self.object})

        nombre_categoria = self.object.nombre
        valor_viejo = f"ID: {self.object.id}, Nombre: {self.object.nombre}"

        response = super().delete(request, *args, **kwargs)

        crear_notificacion_sistema(
            usuario=request.user,
            accion="CATEGORIA ELIMINADA",
            tabla_afectada="Categorías",
            observacion=f"Se ha quitado del sistema la categoría: '{nombre_categoria}'.",
            valor_anterior=valor_viejo,
            nuevo_valor="Registro Eliminado"
        )
        return response


# ==========================================
# TARIFAS
# ==========================================

class TarifaListView(StaffRequiredMixin, ListView):
    model = Tarifa
    template_name = 'admin/tarifas/tarifas.html'
    context_object_name = 'tarifas'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('paquete', 'temporada')
        paquete_id = self.request.GET.get('paquete', '').strip()
        if paquete_id:
            try:
                p_id = int(paquete_id)
                if p_id > 0:
                    queryset = queryset.filter(paquete_id=p_id)
            except (ValueError, TypeError):
                pass
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Tarifa.objects.aggregate(
            total=Count('id'),
            activas=Count('id', filter=Q(estado='activa')),
            inactivas=Count('id', filter=Q(estado='inactiva'))
        )
        context.update(stats)
        context['stats_list'] = [
            ('Total', stats['total'], 'text-dark'),
            ('Activas', stats['activas'], 'text-success'),
            ('Inactivas', stats['inactivas'], 'text-danger'),
        ]
        context['paquetes'] = Paquete.objects.all()
        context['paquete_seleccionado'] = self.request.GET.get('paquete', '')
        return context


class TarifaCreateView(StaffRequiredMixin, CreateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'admin/tarifas/agregar_tarifa.html'
    success_url = reverse_lazy('listar_tarifas')

    def form_valid(self, form):
        # Validar lógica de negocio: Precios no negativos
        precio_adulto = form.cleaned_data.get('precio_adulto')
        precio_menor = form.cleaned_data.get('precio_menor')

        if (precio_adulto is not None and precio_adulto < 0) or (precio_menor is not None and precio_menor < 0):
            form.add_error(None, "Los precios no pueden ser valores negativos.")
            return self.form_invalid(form)

        response = super().form_valid(form)
        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="NUEVA TARIFA CREADA",
            tabla_afectada="Tarifas",
            observacion=f"Se ha registrado una tarifa para el paquete: {self.object.paquete}.",
            valor_anterior="Ninguno (Registro Nuevo)",
            nuevo_valor=f"Adulto: ${self.object.precio_adulto}, Menor: ${self.object.precio_menor}"
        )
        return response

 
class TarifaUpdateView(StaffRequiredMixin, UpdateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'admin/tarifas/editar_tarifa.html'
    success_url = reverse_lazy('listar_tarifas')

    def form_valid(self, form):
        precio_adulto = form.cleaned_data.get('precio_adulto')
        precio_menor = form.cleaned_data.get('precio_menor')

        if (precio_adulto is not None and precio_adulto < 0) or (precio_menor is not None and precio_menor < 0):
            form.add_error(None, "Los precios no pueden ser valores negativos.")
            return self.form_invalid(form)

        tarifa_antigua = self.get_object()
        valor_viejo = f"Adulto: ${tarifa_antigua.precio_adulto}, Menor: ${tarifa_antigua.precio_menor}, Estado: {tarifa_antigua.estado}"

        response = super().form_valid(form)

        valor_nuevo = f"Adulto: ${self.object.precio_adulto}, Menor: ${self.object.precio_menor}, Estado: {self.object.estado}"

        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="TARIFA MODIFICADA",
            tabla_afectada="Tarifas",
            observacion=f"Los datos de la tarifa de '{self.object.paquete}' han sido actualizados.",
            valor_anterior=valor_viejo,
            nuevo_valor=valor_nuevo
        )
        return response


# ==========================================
# TEMPORADAS
# ==========================================

class TemporadaListView(StaffRequiredMixin, ListView):
    model = Temporada
    template_name = 'admin/temporada/temporada.html'
    context_object_name = 'temporadas'

    def get_queryset(self):
        queryset = Temporada.objects.all()
        fecha_inicio = self.request.GET.get("fecha_inicio", "").strip()
        fecha_fin = self.request.GET.get("fecha_fin", "").strip()

      
        if fecha_inicio:
            try:
                f_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_inicio__gte=f_inicio)
            except ValueError:
                pass

        if fecha_fin:
            try:
                f_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_fin__lte=f_fin)
            except ValueError:
                pass

        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Temporada.objects.aggregate(
            total=Count('id'),
            programadas=Count('id', filter=Q(estado='programada')),
            activas=Count('id', filter=Q(estado='activa')),
            finalizadas=Count('id', filter=Q(estado='finalizada'))
        )
        context.update(stats)
        context['stats_list'] = [
            ('Total', stats['total'], 'text-dark'),
            ('Programadas', stats['programadas'], 'text-secondary'),
            ('Activas', stats['activas'], 'text-success'),
            ('Finalizadas', stats['finalizadas'], 'text-info'),
        ]
        return context


class TemporadaCreateView(StaffRequiredMixin, CreateView):
    model = Temporada
    form_class = TemporadaForm
    template_name = 'admin/temporada/agregar_temporada.html'
    success_url = reverse_lazy('listar_temporadas')

    def form_valid(self, form):
        # Validar que fecha_fin no sea anterior a fecha_inicio
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            form.add_error('fecha_fin', "La fecha de finalización no puede ser anterior a la fecha de inicio.")
            return self.form_invalid(form)

        response = super().form_valid(form)
        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="NUEVA TEMPORADA CREADA",
            tabla_afectada="Temporadas",
            observacion=f"Se ha registrado con éxito la temporada: '{self.object.nombre}'.",
            valor_anterior="Ninguno (Registro Nuevo)",
            nuevo_valor=f"Nombre: {self.object.nombre}, Inicio: {self.object.fecha_inicio}, Fin: {self.object.fecha_fin}"
        )
        return response


class TemporadaUpdateView(StaffRequiredMixin, UpdateView):
    model = Temporada
    form_class = TemporadaForm
    template_name = 'admin/temporada/editar_temporada.html'
    success_url = reverse_lazy('listar_temporadas')

    def form_valid(self, form):
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            form.add_error('fecha_fin', "La fecha de finalización no puede ser anterior a la fecha de inicio.")
            return self.form_invalid(form)

        temp_antigua = self.get_object()
        valor_viejo = f"Nombre: {temp_antigua.nombre}, Inicio: {temp_antigua.fecha_inicio}, Fin: {temp_antigua.fecha_fin}, Estado: {temp_antigua.estado}"

        response = super().form_valid(form)

        valor_nuevo = f"Nombre: {self.object.nombre}, Inicio: {self.object.fecha_inicio}, Fin: {self.object.fecha_fin}, Estado: {self.object.estado}"

        crear_notificacion_sistema(
            usuario=self.request.user,
            accion="TEMPORADA MODIFICADA",
            tabla_afectada="Temporadas",
            observacion=f"La temporada '{self.object.nombre}' ha sido actualizada correctamente.",
            valor_anterior=valor_viejo,
            nuevo_valor=valor_nuevo
        )
        return response