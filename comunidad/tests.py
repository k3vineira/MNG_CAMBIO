from django.test import TestCase
from django.urls import reverse
from usuarios.models import Usuario, Cliente
from catalogo.models import Categoria, Paquete
from comunidad.models import Calificacion, Blog, PQRS, Resena, Comentario
import datetime


def crear_usuario(username='testuser', rol=Usuario.Roles.CLIENTE):
    """
    crear_usuario.
    
    :param username='testuser': Descripción del parámetro.
    
    :param rol=Usuario.Roles.CLIENTE: Descripción del parámetro.
    
    :return: Respuesta de la función.
    """
    import random
    return Usuario.objects.create_user(
        username=username,
        password='pass123',
        email=f'{username}@test.com',
        first_name='Comunidad',
        last_name='User',
        tipo_documento='CC',
        numero_documento=f'444{random.randint(100000, 999999)}',
        telefono='3130000000',
        rol=rol
    )


def crear_cliente(username='cliente_test'):
    """
    crear_cliente.
    
    :param username='cliente_test': Descripción del parámetro.
    
    :return: Respuesta de la función.
    """
    usuario = crear_usuario(username=username)
    return Cliente.objects.create(usuario=usuario)


def crear_paquete():
    """
    crear_paquete.
    
    :return: Respuesta de la función.
    """
    cat = Categoria.objects.create(nombre='Test Cat', descripcion='Desc')
    return Paquete.objects.create(
        nombre='Paquete Test',
        descripcion='Desc',
        dias_duracion=1,
        noches_duracion=0,
        punto_encuentro='Plaza',
        hora_encuentro=datetime.time(8, 0),
        categoria=cat
    )


from reservas.models import Reserva

def crear_reserva(usuario, paquete):
    """Auxiliar para crear una reserva de prueba."""
    return Reserva.objects.create(
        usuario=usuario,
        paquete=paquete,
        fecha=datetime.date.today(),
        monto_total=100000
    )


# ──────────────────────────────────────────────────────────────────────────────
# TESTS DE CALIFICACION
# ──────────────────────────────────────────────────────────────────────────────

class CalificacionTest(TestCase):

    def setUp(self):
        """
        setUp.
        
        :return: Respuesta de la función.
        """
        self.cliente = crear_cliente()
        self.paquete = crear_paquete()
        # Creamos una reserva asociada al usuario de este cliente y al paquete
        self.reserva = crear_reserva(self.cliente.usuario, self.paquete)

    def test_crear_calificacion(self):
        """
        test_crear_calificacion.
        
        :return: Respuesta de la función.
        """
        cal = Calificacion.objects.create(
            usuario=self.cliente.usuario,
            reserva=self.reserva,
            puntaje_estrellas=5,
            comentario='Excelente tour'
        )
        self.assertEqual(cal.puntaje_estrellas, 5)
        self.assertEqual(cal.comentario, 'Excelente tour')
        self.assertEqual(cal.reserva, self.reserva)
        self.assertEqual(cal.usuario, self.cliente.usuario)

    def test_multiples_calificaciones_mismo_plan(self):
        """
        Verifica que se puedan crear múltiples calificaciones para la misma reserva (1:N).
        """
        cal1 = Calificacion.objects.create(
            usuario=self.cliente.usuario,
            reserva=self.reserva,
            puntaje_estrellas=4,
            comentario='Primer comentario'
        )
        cal2 = Calificacion.objects.create(
            usuario=self.cliente.usuario,
            reserva=self.reserva,
            puntaje_estrellas=3,
            comentario='Segundo comentario'
        )
        self.assertEqual(self.reserva.calificaciones.count(), 2)

    def test_comentario_puede_estar_vacio(self):
        """
        test_comentario_puede_estar_vacio.
        
        :return: Respuesta de la función.
        """
        cal = Calificacion.objects.create(
            usuario=self.cliente.usuario,
            reserva=self.reserva,
            puntaje_estrellas=3,
            comentario=''
        )
        self.assertEqual(cal.comentario, '')



# ──────────────────────────────────────────────────────────────────────────────
# TESTS DE BLOG
# ──────────────────────────────────────────────────────────────────────────────

class BlogTest(TestCase):

    def setUp(self):
        self.usuario = crear_usuario(username='autor_blog')

    def test_crear_blog(self):
        blog = Blog.objects.create(
            usuario=self.usuario,
            titulo='Guía de Monagua',
            contenido='Contenido del artículo de prueba',
            estado=True
        )
        self.assertEqual(blog.titulo, 'Guía de Monagua')
        self.assertTrue(blog.estado)

    def test_str_blog(self):
        blog = Blog.objects.create(
            usuario=self.usuario,
            titulo='Primer Post',
            contenido='Texto de prueba'
        )
        self.assertIn('Primer Post', str(blog))

    def test_publicado_default_true(self):
        blog = Blog.objects.create(usuario=self.usuario, titulo='Post', contenido='Texto')
        self.assertTrue(blog.estado)

    def test_get_absolute_url(self):
        blog = Blog.objects.create(usuario=self.usuario, titulo='URL Test', contenido='Texto')
        url = blog.get_absolute_url()
        self.assertIn(str(blog.pk), url)

    def test_ordenamiento_por_fecha_descendente(self):
        b1 = Blog.objects.create(usuario=self.usuario, titulo='Primero', contenido='a')
        b2 = Blog.objects.create(usuario=self.usuario, titulo='Segundo', contenido='b')
        blogs = list(Blog.objects.all())
        # El más reciente (b2) debe aparecer primero
        self.assertEqual(blogs[0].pk, b2.pk)


# ──────────────────────────────────────────────────────────────────────────────
# TESTS DE PQRS
# ──────────────────────────────────────────────────────────────────────────────

class PQRSTest(TestCase):

    def setUp(self):
        """
        setUp.
        
        :return: Respuesta de la función.
        """
        self.cliente = crear_cliente(username='pqrs_user')

    def test_crear_pqrs(self):
        """
        test_crear_pqrs.
        
        :return: Respuesta de la función.
        """
        pqrs = PQRS.objects.create(
            cliente=self.cliente,
            tipo='queja',
            asunto='Problema con la reserva',
            descripcion='Descripción detallada del problema'
        )
        self.assertEqual(pqrs.tipo, 'queja')
        self.assertEqual(pqrs.estado, 'abierto')

    def test_estado_default_abierto(self):
        """
        test_estado_default_abierto.
        
        :return: Respuesta de la función.
        """
        pqrs = PQRS.objects.create(
            tipo='sugerencia',
            asunto='Sugerencia',
            descripcion='Texto'
        )
        self.assertEqual(pqrs.estado, 'abierto')

    def test_pqrs_sin_cliente(self):
        """
        test_pqrs_sin_cliente.
        
        :return: Respuesta de la función.
        """
        pqrs = PQRS.objects.create(
            cliente=None,
            tipo='peticion',
            asunto='Asunto anonimo',
            descripcion='Texto anonimo'
        )
        self.assertIsNone(pqrs.cliente)

    def test_choices_tipo_validos(self):
        """
        test_choices_tipo_validos.
        
        :return: Respuesta de la función.
        """
        tipos = [t[0] for t in PQRS.TIPO_CHOICES]
        for tipo in ['peticion', 'queja', 'reclamo', 'sugerencia']:
            self.assertIn(tipo, tipos)

    def test_choices_estado_validos(self):
        """
        test_choices_estado_validos.
        
        :return: Respuesta de la función.
        """
        estados = [e[0] for e in PQRS.ESTADO_CHOICES]
        for estado in ['abierto', 'en_proceso', 'cerrado']:
            self.assertIn(estado, estados)


# ──────────────────────────────────────────────────────────────────────────────
# TESTS DE COMENTARIO
# ──────────────────────────────────────────────────────────────────────────────

class ComentarioTest(TestCase):

    def setUp(self):
        """
        setUp.
        
        :return: Respuesta de la función.
        """
        self.usuario = crear_usuario(username='comentador')
        self.paquete = crear_paquete()

    def test_crear_comentario_con_paquete(self):
        """
        test_crear_comentario_con_paquete.
        
        :return: Respuesta de la función.
        """
        com = Comentario.objects.create(
            usuario=self.usuario,
            tipo='experiencia',
            titulo='Increíble',
            mensaje='Fue una experiencia maravillosa.',
            valoracion=5,
            paquete=self.paquete
        )
        self.assertEqual(com.valoracion, 5)
        self.assertTrue(com.visible)

    def test_crear_comentario_sin_paquete(self):
        """
        test_crear_comentario_sin_paquete.
        
        :return: Respuesta de la función.
        """
        com = Comentario.objects.create(
            usuario=self.usuario,
            mensaje='Comentario general'
        )
        self.assertIsNone(com.paquete)

    def test_str_comentario(self):
        """
        test_str_comentario.
        
        :return: Respuesta de la función.
        """
        com = Comentario.objects.create(
            usuario=self.usuario,
            titulo='Mi título',
            mensaje='Texto'
        )
        self.assertIn(self.usuario.username, str(com))
        self.assertIn('Mi título', str(com))

    def test_str_comentario_sin_titulo(self):
        """
        test_str_comentario_sin_titulo.
        
        :return: Respuesta de la función.
        """
        com = Comentario.objects.create(
            usuario=self.usuario,
            mensaje='Sin título'
        )
        self.assertIn(self.usuario.username, str(com))

    def test_visible_default_true(self):
        """
        test_visible_default_true.
        
        :return: Respuesta de la función.
        """
        com = Comentario.objects.create(
            usuario=self.usuario,
            mensaje='Visible'
        )
        self.assertTrue(com.visible)

    def test_valoracion_default_cinco(self):
        """
        test_valoracion_default_cinco.
        
        :return: Respuesta de la función.
        """
        com = Comentario.objects.create(
            usuario=self.usuario,
            mensaje='Con valoración default'
        )
        self.assertEqual(com.valoracion, 5)

    def test_ordenamiento_descendente_por_fecha(self):
        """
        test_ordenamiento_descendente_por_fecha.
        
        :return: Respuesta de la función.
        """
        c1 = Comentario.objects.create(usuario=self.usuario, mensaje='Primero')
        c2 = Comentario.objects.create(usuario=self.usuario, mensaje='Segundo')
        comentarios = list(Comentario.objects.all())
        self.assertEqual(comentarios[0].pk, c2.pk)

# ──────────────────────────────────────────────────────────────────────────────
# TESTS DE VISTAS DE COMENTARIO
# ──────────────────────────────────────────────────────────────────────────────

class ComentarioViewsTest(TestCase):

    def setUp(self):
        self.cliente = crear_cliente(username='cliente_vistas')
        self.admin = crear_usuario(username='admin_vistas')
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.save()
        self.paquete = crear_paquete()
        
    def test_mis_resenas_get(self):
        self.client.force_login(self.cliente.usuario)
        response = self.client.get(reverse('mis_resenas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comunidad/private_resenas.html')

    def test_mis_resenas_post(self):
        self.client.force_login(self.cliente.usuario)
        data = {
            'tipo': 'experiencia',
            'titulo': 'Excelente',
            'mensaje': 'Muy buen paquete',
            'valoracion': 5,
            'paquete_id': self.paquete.id
        }
        response = self.client.post(reverse('mis_resenas'), data)
        self.assertRedirects(response, reverse('mis_resenas'))
        self.assertTrue(Comentario.objects.filter(titulo='Excelente').exists())
        
    def test_listar_comentarios_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('listar_comentarios'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comunidad/admin_comentarios.html')
        
    def test_toggle_visible(self):
        com = Comentario.objects.create(usuario=self.cliente.usuario, paquete=self.paquete, mensaje="test", visible=True)
        self.client.force_login(self.admin)
        response = self.client.post(reverse('toggle_visible', args=[com.pk]))
        self.assertRedirects(response, reverse('listar_comentarios'))
        com.refresh_from_db()
        self.assertFalse(com.visible)

    def test_responder_comentario(self):
        com = Comentario.objects.create(usuario=self.cliente.usuario, paquete=self.paquete, mensaje="test")
        self.client.force_login(self.admin)
        data = {'admin_respuesta': 'Gracias por comentar'}
        response = self.client.post(reverse('responder_comentario', args=[com.pk]), data)
        self.assertRedirects(response, reverse('listar_comentarios'))
        com.refresh_from_db()
        self.assertEqual(com.admin_respuesta, 'Gracias por comentar')
