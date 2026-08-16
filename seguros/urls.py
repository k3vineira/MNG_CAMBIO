from django.urls import path
from . import views

urlpatterns = [
    path('planes/', views.lista_seguros, name='lista_seguros'),
    path('adquirir/<int:reserva_id>/', views.adquirir_seguro, name='adquirir_seguro'),
]
