"""
Vistas principales del núcleo de la aplicación, incluyendo la página de inicio.
"""

from django.shortcuts import render
from promociones.models import Banner

def inicio(request):
    """
    Renderiza la página de inicio pública del sitio Monagua.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: La página de inicio renderizada.
    """
    banners_activos = Banner.objects.filter(activo=True)
    
    context = {
        'titulo': 'Monagua — Agencia de Viajes y Turismo',
        'banners': banners_activos
    }
    return render(request, 'index.html', context)
