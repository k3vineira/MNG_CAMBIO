"""
Formularios para la gestión de reservas y cancelaciones de paquetes turísticos.
"""

import re
from datetime import date, timedelta
from django import forms
from django.forms import ModelForm, Select, DateInput, NumberInput
from django.core.exceptions import ValidationError
from .models import Reserva, Cancelacion


class ReservaForm(ModelForm):
    """Formulario para la creación y edición de reservas."""

    class Meta:
        model = Reserva
        fields = ['cliente', 'paquete', 'fecha', 'numero_adultos', 'numero_menores']
        widgets = {
            'cliente': Select(attrs={'class': 'form-select'}),
            'paquete': Select(attrs={'class': 'form-select'}),
            'fecha': DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'numero_adultos': NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'numero_menores': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se exige al menos 2 días de anticipación desde el día actual
        fecha_minima = date.today() + timedelta(days=2)
        self.fields['fecha'].widget.attrs['min'] = fecha_minima.strftime('%Y-%m-%d')

    def clean_fecha(self):
        fecha_reserva = self.cleaned_data.get('fecha')
        fecha_minima = date.today() + timedelta(days=2)

        if fecha_reserva:
            if fecha_reserva < date.today():
                raise ValidationError("No puedes seleccionar una fecha pasada.")
            
            if fecha_reserva < fecha_minima:
                raise ValidationError(
                    f"La reserva debe realizarse con al menos 2 días de anticipación "
                    f"(a partir del {fecha_minima.strftime('%d/%m/%Y')})."
                )

        return fecha_reserva

    def clean_numero_adultos(self):
        adultos = self.cleaned_data.get('numero_adultos')
        if adultos is None or adultos < 1:
            raise ValidationError("Debe haber al menos 1 adulto en la reserva.")
        return adultos

    def clean_numero_menores(self):
        menores = self.cleaned_data.get('numero_menores')
        if menores is None or menores < 0:
            raise ValidationError("El número de menores no puede ser negativo.")
        return menores

    def clean(self):
        cleaned_data = super().clean()
        adultos = cleaned_data.get('numero_adultos') or 0
        menores = cleaned_data.get('numero_menores') or 0

        # Validamos la capacidad total (al menos 1 persona presente)
        if adultos + menores <= 0:
            raise ValidationError("La reserva debe incluir al menos una persona.")

        return cleaned_data


class CancelacionForm(ModelForm):
    """Formulario para la gestión de solicitudes de cancelación."""

    class Meta:
        model = Cancelacion
        fields = ['reserva', 'motivo']
        widgets = {
            'reserva': forms.Select(attrs={
                'class': 'form-control bg-light',
                'style': 'pointer-events: none;',
                'readonly': 'readonly'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Explica detalladamente el motivo de la cancelación...'
            }),
        }

    def clean_motivo(self):
        motivo = str(self.cleaned_data.get('motivo', '')).strip()

        if not motivo:
            raise ValidationError("Debes ingresar un motivo para cancelar la reserva.")

        if len(motivo) < 10:
            raise ValidationError("Por favor, detalla un poco más el motivo (mínimo 10 caracteres).")

        if motivo.isdigit():
            raise ValidationError("El motivo de cancelación debe contener texto descriptivo, no solo números.")

        if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', motivo):
            raise ValidationError("El motivo de cancelación debe incluir letras.")

        return motivo