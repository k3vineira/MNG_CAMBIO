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
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


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
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'dias_duracion': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'noches_duracion': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
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
        # La imagen solo es obligatoria al CREAR un paquete nuevo.
        # Si se está EDITANDO (instance.pk existe), no obliga a resubir la imagen.
        if not self.instance.pk:
            self.fields['imagen'].required = True
            self.fields['imagen'].widget.attrs['required'] = 'required'

    
    def clean_punto_encuentro(self):
        punto = str(self.cleaned_data.get('punto_encuentro', '')).strip()

        # Verifica si son solo números (ej: "123", "4567")
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
        if noches is None or noches < 1:
            raise ValidationError("Las noches de duración deben ser al menos 1.")
        return noches

class TarifaForm(ModelForm):
    """Formulario para crear y editar tarifas asociadas a un paquete y temporada."""
    class Meta:
        model = Tarifa
        exclude = ['estado']
        widgets = {
            'paquete': forms.Select(attrs={'class': 'form-select'}),
            'temporada': forms.Select(attrs={'class': 'form-select'}),
            'precio_adulto': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_menor': forms.NumberInput(attrs={'class': 'form-control'}),
        }


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
