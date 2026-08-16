from django.test import TestCase
from django.contrib.auth import get_user_model
from auditoria.models import Auditoria
from auditoria.utils import crear_notificacion_sistema

Usuario = get_user_model()

class AuditoriaTestCase(TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = Usuario.objects.create_user(
            username='user_notif',
            email='user@notif.com',
            password='password123'
        )

    def test_crear_notificacion_sistema_exito(self):
        # Crear notificación utilizando el utilitario
        notificacion = crear_notificacion_sistema(
            usuario=self.user,
            titulo="Nueva Alerta",
            mensaje="Esto es un mensaje de alerta de prueba.",
            tipo="sistema"
        )
        
        self.assertIsNotNone(notificacion)
        self.assertEqual(notificacion.codigo_usuario, self.user)
        self.assertEqual(notificacion.acciones_realizada, "Nueva Alerta")
        self.assertEqual(notificacion.observacion, "Esto es un mensaje de alerta de prueba.")
        self.assertEqual(notificacion.tabla_afectada, "Sistema")

    def test_crear_notificacion_usuario_no_autenticado(self):
        # Si pasamos un usuario no autenticado (o None), debe retornar None
        notificacion = crear_notificacion_sistema(
            usuario=None,
            titulo="Alerta Anónima",
            mensaje="Prueba anónima.",
            tipo="sistema"
        )
        self.assertIsNone(notificacion)

    def test_crear_auditoria_directa(self):
        auditoria = Auditoria.objects.create(
            codigo_usuario=self.user,
            acciones_realizada="Reserva Confirmada",
            observacion="Tu reserva #123 ha sido confirmada.",
            tabla_afectada="reserva"
        )
        
        self.assertEqual(auditoria.codigo_usuario, self.user)
        self.assertEqual(auditoria.acciones_realizada, "Reserva Confirmada")
