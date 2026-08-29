from django import forms
from .models import Aseguradora, PolizaViaje

class PolizaForm(forms.ModelForm):
    class Meta:
        model = PolizaViaje
        fields = ['aseguradora']
        widgets = {
            'aseguradora': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['aseguradora'].queryset = Aseguradora.objects.filter(estado=True)
