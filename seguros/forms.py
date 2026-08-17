from django import forms
from .models import Poliza, SeguroViaje

class SeguroViajeForm(forms.ModelForm):
    class Meta:
        model = SeguroViaje
        fields = ['poliza']
        widgets = {
            'poliza': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar únicamente seguros/pólizas activas en el formulario
        self.fields['poliza'].queryset = Poliza.objects.filter(estado=True)
