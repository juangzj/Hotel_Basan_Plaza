from django.db import models
from habitaciones.models.models import Habitacion


# Tarifas
class Tarifa(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"Habitación {self.habitacion.id} - ${self.precio_por_noche} - {self.descripcion}"
