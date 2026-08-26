from django.http import HttpResponseForbidden
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class AntiTamperingMiddleware:
    """
    Middleware para detectar y bloquear intentos de enviar valores numéricos negativos
    (como montos, penalidades, cantidad de personas) a través de herramientas 
    como el Inspector de elementos, Postman o cURL.
    
    Además, incluye protección básica contra fuerza bruta usando la IP.
    """
    
    # Campos que deben ser estrictamente >= 0
    CAMPOS_PROTEGIDOS = [
        'monto', 
        'valor_subtotal', 
        'valor_total', 
        'numero_adultos', 
        'numero_menores', 
        'penalidad',
        'valor_reembolsado'
    ]
    
    # Configuración de bloqueo
    MAX_INTENTOS = 3
    TIEMPO_BLOQUEO = 60 * 15  # 15 minutos en segundos

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_cliente = self.obtener_ip_cliente(request)
        cache_key = f"bloqueo_tampering_{ip_cliente}"

        # 1. Verificar si la IP ya está bloqueada
        if cache.get(cache_key) == 'bloqueado':
            logger.warning(f"Intento de acceso desde IP bloqueada por tampering: {ip_cliente}")
            return HttpResponseForbidden(
                "Tu dirección IP ha sido temporalmente bloqueada por actividad sospechosa."
            )

        # 2. Interceptar solo peticiones POST
        if request.method == 'POST':
            es_manipulacion = self.verificar_manipulacion_datos(request.POST)

            if es_manipulacion:
                # Incrementar contador de intentos fallidos
                intentos_key = f"intentos_tampering_{ip_cliente}"
                intentos = cache.get(intentos_key, 0) + 1
                cache.set(intentos_key, intentos, timeout=self.TIEMPO_BLOQUEO)
                
                logger.warning(f"Detección de manipulación de datos desde IP: {ip_cliente} (Intento {intentos})")

                if intentos >= self.MAX_INTENTOS:
                    # Bloquear IP
                    cache.set(cache_key, 'bloqueado', timeout=self.TIEMPO_BLOQUEO)
                    logger.error(f"IP {ip_cliente} bloqueada por múltiples intentos de manipulación.")
                    return HttpResponseForbidden(
                        "Has superado el límite de intentos maliciosos. Tu IP ha sido bloqueada por 15 minutos."
                    )
                
                return HttpResponseForbidden(
                    "Operación rechazada: Se han detectado valores inválidos (negativos) en la solicitud. "
                    "Este incidente ha sido registrado."
                )

        # 3. Continuar con el flujo normal si todo está bien
        response = self.get_response(request)
        return response

    def verificar_manipulacion_datos(self, post_data):
        """Revisa si algún campo protegido contiene un valor menor a cero."""
        for campo in self.CAMPOS_PROTEGIDOS:
            if campo in post_data:
                valor_str = post_data.get(campo)
                try:
                    # Intentamos convertirlo a float para verificar su valor real
                    valor = float(valor_str)
                    if valor < 0:
                        return True
                except (ValueError, TypeError):
                    # Si no es un número, lo ignoramos aquí (la validación del formulario de Django se encargará de esto)
                    pass
        return False

    def obtener_ip_cliente(self, request):
        """Obtiene la IP real del cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
