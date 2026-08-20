import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from catalogo.models import Categoria, Paquete, Temporada, Tarifa
from promociones.models import Promocion, PaquetePromocion, Banner

class PromocionesTestCase(TestCase):
    def setUp(self):
        """
        setUp.
        
        :return: Respuesta de la función.
        """
        from usuarios.models import Usuario
        self.admin = Usuario.objects.create_superuser(
            username='admin_promo',
            email='admin@promo.com',
            password='password123',
            first_name='Admin',
            last_name='Promo',
            tipo_documento='CC',
            numero_documento='222111000',
            telefono='3150000000',
            rol='admin'
        )
        self.client.force_login(self.admin)
        self.categoria = Categoria.objects.create(
            nombre='Playas',
            descripcion='Tours de playa'
        )
        self.paquete = Paquete.objects.create(
            nombre='Especial Cartagena',
            descripcion='Tour por la ciudad amurallada',
            dias_duracion=3,
            noches_duracion=2,
            punto_encuentro='Aeropuerto',
            hora_encuentro=datetime.time(10, 0),
            categoria=self.categoria
        )
        self.temporada = Temporada.objects.create(
            nombre='Alta Verano',
            fecha_inicio=timezone.now().date() - datetime.timedelta(days=10),
            fecha_fin=timezone.now().date() + datetime.timedelta(days=50),
            descripcion='Temporada vacacional alta'
        )
        self.tarifa = Tarifa.objects.create(
            paquete=self.paquete,
            temporada=self.temporada,
            precio_adulto=100000,
            precio_menor=50000,
            estado='activa'
        )

    def test_crear_promocion(self):
        """
        test_crear_promocion.
        
        :return: Respuesta de la función.
        """
        fecha_inicio = timezone.now().date()
        fecha_fin = timezone.now().date() + datetime.timedelta(days=7)
        promo = Promocion.objects.create(
            nombre='Descuento de Temporada',
            descripcion='Disfruta de Cartagena con un 15% de descuento.',
            descuento=15,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            codigo_promocion='PROM-1111',
            activa=True
        )
        pp = PaquetePromocion.objects.create(
            paquete=self.paquete,
            promocion=promo,
            tarifa=self.tarifa
        )
        self.assertEqual(promo.nombre, 'Descuento de Temporada')
        self.assertEqual(promo.descuento, 15)
        self.assertTrue(promo.activa)
        self.assertEqual(str(promo), 'Descuento de Temporada (15%)')
        self.assertEqual(pp.paquete, self.paquete)
        self.assertEqual(pp.promocion, promo)

    def test_crear_banner(self):
        """
        test_crear_banner.
        
        :return: Respuesta de la función.
        """
        banner = Banner.objects.create(
            imagen='banners/test_banner.jpg',
            titulo='Banner Principal',
            enlace='https://example.com/promo',
            activo=True
        )
        self.assertEqual(banner.titulo, 'Banner Principal')
        self.assertEqual(banner.enlace, 'https://example.com/promo')
        self.assertTrue(banner.activo)
        self.assertEqual(str(banner), 'Banner Principal')

    def test_gestion_promociones_view(self):
        """
        test_gestion_promociones_view.
        
        :return: Respuesta de la función.
        """
        fecha_inicio = timezone.now().date()
        fecha_fin = timezone.now().date() + datetime.timedelta(days=5)
        promo = Promocion.objects.create(
            nombre='Super Promo',
            descripcion='Super descuento',
            descuento=20,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            codigo_promocion='PROM-2222',
            activa=True
        )
        PaquetePromocion.objects.create(
            paquete=self.paquete,
            promocion=promo,
            tarifa=self.tarifa
        )
        response = self.client.get(reverse('gestion_promociones'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Super Promo')
        self.assertContains(response, 'Ofertas de Temporada')
