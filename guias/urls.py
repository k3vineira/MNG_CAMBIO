from django.urls import path
from . import views

urlpatterns = [
    path('asignaciones/', views.listar_planes_guia, name='listar_planes_guia'),
    path('asignaciones/crear/', views.crear_plan_guia, name='crear_plan_guia'),
    path('asignaciones/editar/<int:pk>/', views.editar_plan_guia, name='editar_plan_guia'),
    path('asignaciones/eliminar/<int:pk>/', views.eliminar_plan_guia, name='eliminar_plan_guia'),
]
