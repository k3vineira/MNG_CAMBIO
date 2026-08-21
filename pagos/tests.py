import datetime
from django.test import TestCase
from django.utils import timezone
from usuarios.models import Usuario
from catalogo.models import Categoria, Paquete, Temporada, Tarifa
from reservas.models import Reserva
from pagos.models import Pago


def crear_usuario(username='pago_user'):
    """
    crear_usuario.
    
    :param username='pago_user': Descripción del parámetro.
    
    :return: Respuesta de la función.
    """
    import random
    return Usuario.objects.create_user(
        username=username,
        password='pass123',
        email=f'{username}@test.com',
        first_name='Pago',
        last_name='User',
        tipo_documento='CC',
        numero_documento=f'555{random.randint(100000, 999999)}',
        telefono='3120000000'
    )


def crear_paquete():
    """
    crear_paquete.
    
    :return: Respuesta de la función.
    """
    cat = Categoria.objects.create(nombre='Cat Pagos', descripcion='Desc')
    return Paquete.objects.create(
        nombre='Paquete Pagos',
        descripcion='Desc',
        dias_duracion=2,
        noches_duracion=1,
        punto_encuentro='Plaza',
        hora_encuentro=datetime.time(9, 0),
        categoria=cat
    )


def crear_reserva(usuario, paquete):
    """
    crear_reserva.
    
    :param usuario: Descripción del parámetro.
    
    :param paquete: Descripción del parámetro.
    
    :return: Respuesta de la función.
    """
    fecha = timezone.now().date() + datetime.timedelta(days=30)
    return Reserva.objects.create(
        usuario=usuario,
        paquete=paquete,
        fecha=fecha,
        numero_adultos=1
    )


# ──────────────────────────────────────────────────────────────────────────────
# TESTS DE PAGO
# ──────────────────────────────────────────────────────────────────────────────

class PagoCreacionTest(TestCase):

    def setUp(self):
        """
        setUp.
        
        :return: Respuesta de la función.
        """
        self.usuario = crear_usuario()
        self.paquete = crear_paquete()
        self.reserva = crear_reserva(self.usuario, self.paquete)

    def test_crear_comprobante_estado_pendiente(self):
        """
        test_crear_comprobante_estado_pendiente.
        
        :return: Respuesta de la función.
        """
        comp = Pago.objects.create(
            usuario=self.usuario,
            reserva=self.reserva,
            referencia='REF-001',
            banco_origen='Bancolombia',
            monto=200000,
            imagen_comprobante='comprobantes/test.jpg',
            descripcion='Pago de prueba'
        )
        self.assertEqual(comp.estado_transaccion, 'pendiente')
        self.assertTrue(comp.pk)

    def test_str_comprobante(self):
        """
        test_str_comprobante.
        
        :return: Respuesta de la función.
        """
        comp = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/test.jpg'
        )
        resultado = str(comp)
        self.assertIn(self.usuario.username, resultado)
        self.assertIn('Pendiente', resultado)

    def test_estado_default_pendiente(self):
        """
        test_estado_default_pendiente.
        
        :return: Respuesta de la función.
        """
        comp = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/test.jpg'
        )
        self.assertEqual(comp.estado_transaccion, 'pendiente')

    def test_reserva_puede_ser_nula(self):
        """
        test_reserva_puede_ser_nula.
        
        :return: Respuesta de la función.
        """
        comp = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/test.jpg',
            reserva=None
        )
        self.assertIsNone(comp.reserva)


class PagoEstadosTest(TestCase):

    def setUp(self):
        """
        setUp.
        
        :return: Respuesta de la función.
        """
        self.usuario = crear_usuario('estado_pago')

    def test_choices_estado_validos(self):
        """
        test_choices_estado_validos.
        
        :return: Respuesta de la función.
        """
        estados = [e[0] for e in Pago.ESTADO_CHOICES]
        self.assertIn('pendiente', estados)
        self.assertIn('aprobado', estados)
        self.assertIn('rechazado', estados)

    def test_cambiar_estado_a_aprobado(self):
        """
        test_cambiar_estado_a_aprobado.
        
        :return: Respuesta de la función.
        """
        comp = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/test.jpg'
        )
        comp.banco_origen = 'Bancolombia'
        comp.monto = 200000
        comp.estado_transaccion = 'aprobado'
        comp.save()
        comp.refresh_from_db()
        self.assertEqual(comp.estado_transaccion, 'aprobado')

    def test_validacion_aprobar_sin_banco(self):
        from django.core.exceptions import ValidationError
        comp = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/test.jpg'
        )
        comp.estado_transaccion = 'aprobado'
        comp.monto = 200000
        with self.assertRaises(ValidationError) as context:
            comp.save()
        self.assertIn("Debe especificar el banco de origen", str(context.exception))

    def test_validacion_aprobar_sin_monto(self):
        from django.core.exceptions import ValidationError
        comp = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/test.jpg'
        )
        comp.estado_transaccion = 'aprobado'
        comp.banco_origen = 'Nequi'
        with self.assertRaises(ValidationError) as context:
            comp.save()
        self.assertIn("Debe especificar el monto pagado", str(context.exception))

    def test_validacion_aprobar_monto_insuficiente(self):
        from django.core.exceptions import ValidationError
        paquete = crear_paquete()
        reserva = crear_reserva(self.usuario, paquete)
        
        # Override the recalculation behavior in the test by updating directly in DB
        # since Reserva.save() zeroes it out without valid rates.
        Reserva.objects.filter(pk=reserva.pk).update(monto_total=1000000)
        reserva.refresh_from_db()
        
        comp = Pago.objects.create(
            usuario=self.usuario,
            reserva=reserva,
            imagen_comprobante='comprobantes/test.jpg',
            banco_origen='Nequi',
            monto=500000
        )
        comp.estado_transaccion = 'aprobado'
        with self.assertRaises(ValidationError) as context:
            comp.save()
        self.assertIn("menor al monto total", str(context.exception))

    def test_cambiar_estado_a_rechazado(self):
        """
        test_cambiar_estado_a_rechazado.
        
        :return: Respuesta de la función.
        """
        comp = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/test.jpg'
        )
        comp.estado_transaccion = 'rechazado'
        comp.nota_admin = 'Rechazo de prueba'
        comp.save()
        comp.refresh_from_db()
        self.assertEqual(comp.estado_transaccion, 'rechazado')

    def test_nombre_archivo_sin_imagen(self):
        """
        test_nombre_archivo_sin_imagen.
        
        :return: Respuesta de la función.
        """
        comp = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/recibo.jpg'
        )
        # El método nombre_archivo debe retornar el basename
        self.assertEqual(comp.nombre_archivo(), 'recibo.jpg')

    def test_ordenamiento_por_fecha_envio_descendente(self):
        """
        test_ordenamiento_por_fecha_envio_descendente.
        
        :return: Respuesta de la función.
        """
        comp1 = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/a.jpg'
        )
        comp2 = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/b.jpg'
        )
        comprobantes = list(Pago.objects.all())
        self.assertEqual(comprobantes[0].pk, comp2.pk)

    def test_relacion_usuario_comprobante(self):
        """
        test_relacion_usuario_comprobante.
        
        :return: Respuesta de la función.
        """
        comp = Pago.objects.create(
            usuario=self.usuario,
            imagen_comprobante='comprobantes/test.jpg'
        )
        self.assertIn(comp, self.usuario.comprobantes.all())
