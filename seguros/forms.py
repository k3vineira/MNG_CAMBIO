from django import forms
from .models import Poliza, SeguroViaje

class PolizaForm(forms.ModelForm):
    class Meta:
        model = Poliza
        fields = ['seguro']
        widgets = {
            'seguro': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar únicamente seguros activos en el formulario
        self.fields['seguro'].queryset = SeguroViaje.objects.filter(activo=True)
