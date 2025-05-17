from django.db import models
from habitaciones.models.models import Habitacion
from django.core.exceptions import ValidationError


class Tarifa(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(blank=True)

    def clean(self):
        # Validar que la fecha de inicio sea anterior a la fecha de fin
        if self.fecha_inicio > self.fecha_fin:
            raise ValidationError(
                "La fecha de inicio no puede ser posterior a la fecha de fin."
            )

    def __str__(self):
        return f"Habitación {self.habitacion.id} - ${self.precio_por_noche} - {self.descripcion}"
