from django import forms
from .models import PQRS, Blog


class PqrsForm(forms.ModelForm):
    class Meta:
        model = PQRS

        fields = ['tipo', 'asunto', 'descripcion']
        labels = {
            'tipo': 'Tipo de Solicitud',
            'asunto': 'Asunto de la PQRS',
            'descripcion': 'Detalle de su solicitud',
        }

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Cuéntanos más...'}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titulo', 'contenido',
                  'informacion_adicional', 'imagen_destacada', 'estado']
        labels = {
            'titulo': 'Título del Blog',
            'contenido': 'Contenido del Blog',
            'informacion_adicional': 'Información Adicional',
            'imagen_destacada': 'Imagen del Blog',
            'fecha_publicacion': 'Fecha de Publicación',
            'estado': '¿Publicar ahora?',
        }
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Escribe el contenido del blog aquí...'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
