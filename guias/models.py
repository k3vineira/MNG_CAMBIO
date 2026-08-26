from django.db import models
from django.conf import settings

class PlanGuia(models.Model):
    """
    Modelo que representa la entidad 'plan_guia' del MER.
    Permite asignar un guía turístico a un paquete específico con fechas e idioma de servicio.
    """
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('completado', 'Completado'),
    ]

    idioma_servicio = models.CharField(max_length=50, verbose_name="Idioma del Servicio")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_inicio_plan = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin_plan = models.DateField(verbose_name="Fecha de Fin")
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activo',
        verbose_name="Estado"
    )
    guia = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="planes_guia",
        verbose_name="Guía Turístico (Usuario)"
    )

    class Meta:
        db_table = 'plan_guia'
        verbose_name = "Plan Guía"
        verbose_name_plural = "Planes Guía"

    def __str__(self):
        nombre_guia = self.guia.get_full_name() or self.guia.username
        return f"Plan de Guía: {nombre_guia} ({self.fecha_inicio_plan} a {self.fecha_fin_plan})"
