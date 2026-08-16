from django.db import models
from usuarios.models import GuiaTuristico
from catalogo.models import Paquete

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
        GuiaTuristico,
        on_delete=models.CASCADE,
        related_name="planes_guia",
        db_column="codigo_guia_turistico",
        verbose_name="Guía Turístico"
    )
    paquete = models.ForeignKey(
        Paquete,
        on_delete=models.CASCADE,
        related_name="planes_guia",
        db_column="codigo_paquete",
        verbose_name="Paquete"
    )

    class Meta:
        db_table = 'plan_guia'
        verbose_name = "Plan Guía"
        verbose_name_plural = "Planes Guía"

    def __str__(self):
        nombre_guia = self.guia.usuario.nombre_completo
        return f"Guía: {nombre_guia} - Paquete: {self.paquete.nombre} ({self.fecha_inicio_plan} a {self.fecha_fin_plan})"
