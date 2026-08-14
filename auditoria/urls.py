from django.urls import path
from . import views

urlpatterns = [
    path('mis-notificaciones/', views.lista_notificaciones, name='lista_notificaciones'),
    path('marcar/<int:noti_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
]