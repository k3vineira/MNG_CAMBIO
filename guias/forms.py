from django import forms
from django.core.exceptions import ValidationError
from .models import PlanGuia

class PlanGuiaForm(forms.ModelForm):
    class Meta:
        model = PlanGuia
        fields = ['guia', 'paquete', 'fecha_inicio_plan', 'fecha_fin_plan', 'idioma_servicio', 'estado']
        widgets = {
            'guia': forms.Select(attrs={'class': 'form-select'}),
            'paquete': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio_plan': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin_plan': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'idioma_servicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Español, Inglés'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get("fecha_inicio_plan")
        fin = cleaned_data.get("fecha_fin_plan")
        guia = cleaned_data.get("guia")
        estado = cleaned_data.get("estado")

        # 1. Validar orden de las fechas
        if inicio and fin and fin < inicio:
            self.add_error('fecha_fin_plan', "La fecha de fin no puede ser anterior a la de inicio.")

        # 2. Validar que el guía no tenga otro plan activo que se superponga
        if guia and inicio and fin and estado == 'activo':
            overlaps = PlanGuia.objects.filter(
                guia=guia,
                estado='activo',
                fecha_inicio_plan__lte=fin,
                fecha_fin_plan__gte=inicio
            )
            # Si estamos editando un plan existente, lo excluimos de la búsqueda de solapamientos
            if self.instance and self.instance.pk:
                overlaps = overlaps.exclude(pk=self.instance.pk)

            if overlaps.exists():
                self.add_error('guia', "Este guía ya tiene otro paquete activo asignado en este rango de fechas.")

        return cleaned_data
