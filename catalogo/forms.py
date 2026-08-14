"""
Formularios de gestión para el catálogo: categorías, actividades, paquetes, tarifas y temporadas.
"""

import re
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Categoria, Actividades, Paquete, Tarifa, Temporada

class CategoriaForm(ModelForm):
    """Formulario para crear y editar categorías de paquetes turísticos."""

    class Meta:
        model = Categoria
        exclude = ['estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                'title': 'El nombre de la categoría solo debe contener letras, no números.'
            }),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_nombre(self):
        nombre = str(self.cleaned_data.get('nombre', '')).strip()

        if not nombre:
            raise ValidationError("El nombre de la categoría es obligatorio.")

        
        if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', nombre):
            raise ValidationError("El nombre de la categoría debe contener letras.")


        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise ValidationError("El nombre de la categoría solo debe contener letras y espacios, no se permiten números.")

        return nombre

    def clean_descripcion(self):
        descripcion = str(self.cleaned_data.get('descripcion', '')).strip()

        if not descripcion:
            raise ValidationError("La descripción es obligatoria.")

    
        if descripcion.isdigit():
            raise ValidationError("La descripción no puede contener únicamente números.")

        if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', descripcion):
            raise ValidationError("La descripción debe incluir un texto explicativo con letras.")

        return descripcion


class ActividadesForm(ModelForm):
    """Formulario para crear y editar actividades turísticas."""

    class Meta:
        model = Actividades
        exclude = ['estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'nivel_dificultad': forms.Select(attrs={'class': 'form-select'}),
            'apto_para_menores': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'equipo_requerimiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'recomendacion_salud': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_nombre(self):
        nombre = str(self.cleaned_data.get('nombre', '')).strip()

        if not nombre:
            raise ValidationError("El nombre de la actividad es obligatorio.")

        if nombre.isdigit():
            raise ValidationError("El nombre de la actividad no puede ser solo números.")

        if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', nombre):
            raise ValidationError("El nombre de la actividad debe contener letras.")

        return nombre


class PaqueteForm(ModelForm):
    """Formulario para crear y editar paquetes turísticos incluyendo imagen y actividades."""

    class Meta:
        model = Paquete
        exclude = ['estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'pattern': '.*[a-zA-ZáéíóúÁÉÍÓÚñÑ].*',
                'title': 'La descripción debe contener texto y no solo números.'
            }),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'dias_duracion': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'noches_duracion': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'duracion_estimada': forms.TextInput(attrs={'class': 'form-control'}),
            'punto_encuentro': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '.*[a-zA-ZáéíóúÁÉÍÓÚñÑ].*',
                'title': 'El punto de encuentro debe incluir letras o el nombre de un lugar, no solo números.'
            }),
            'hora_encuentro': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'actividades': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['imagen'].required = True
            self.fields['imagen'].widget.attrs['required'] = 'required'

    def clean_nombre(self):
        nombre = str(self.cleaned_data.get('nombre', '')).strip()
        if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', nombre):
            raise ValidationError("El nombre del paquete debe contener texto y no solo números.")
        return nombre

    def clean_descripcion(self):
        descripcion = str(self.cleaned_data.get('descripcion', '')).strip()

        if not descripcion:
            raise ValidationError("La descripción es obligatoria.")

        if descripcion.isdigit():
            raise ValidationError("La descripción no puede contener solo números. Ingresa un texto descriptivo.")

        if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', descripcion):
            raise ValidationError("La descripción debe contener letras y detalles explicativos.")

        return descripcion

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise ValidationError("El precio del paquete debe ser mayor a 0.")
        return precio

    def clean_punto_encuentro(self):
        punto = str(self.cleaned_data.get('punto_encuentro', '')).strip()

        if punto.isdigit():
            raise ValidationError("El punto de encuentro no puede contener solo números. Ingresa un lugar o dirección válida.")

        if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', punto):
            raise ValidationError("El punto de encuentro debe incluir el nombre de un lugar o texto válido.")

        return punto

    def clean_dias_duracion(self):
        dias = self.cleaned_data.get('dias_duracion')
        if dias is None or dias < 1:
            raise ValidationError("Los días de duración deben ser al menos 1.")
        return dias

    def clean_noches_duracion(self):
        noches = self.cleaned_data.get('noches_duracion')
        if noches is None or noches < 0:
            raise ValidationError("Las noches de duración no pueden ser un valor negativo.")
        return noches
    
class TarifaForm(ModelForm):
    """Formulario para crear y editar tarifas asociadas a un paquete y temporada."""

    class Meta:
        model = Tarifa
        exclude = ['estado']
        widgets = {
            'paquete': forms.Select(attrs={'class': 'form-select'}),
            'temporada': forms.Select(attrs={'class': 'form-select'}),
            'precio_adulto': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'precio_menor': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def clean_precio_adulto(self):
        precio = self.cleaned_data.get('precio_adulto')
        if precio is not None and precio <= 0:
            raise ValidationError("El precio para adulto debe ser mayor a 0.")
        return precio

    def clean_precio_menor(self):
        precio = self.cleaned_data.get('precio_menor')
        if precio is not None and precio < 0:
            raise ValidationError("El precio para menor no puede ser un valor negativo.")
        return precio


class TemporadaForm(ModelForm):
    """Formulario para crear y editar temporadas turísticas con fechas de vigencia."""

    class Meta:
        model = Temporada
        fields = ['nombre', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'fecha_fin': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

    def clean_nombre(self):
        nombre = str(self.cleaned_data.get('nombre', '')).strip()
        if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', nombre):
            raise ValidationError("El nombre de la temporada debe contener letras (ej: 'Temporada Alta 2026').")
        return nombre

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")

        return cleaned_data
    