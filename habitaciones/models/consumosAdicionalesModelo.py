from django.db import models
from habitaciones.models.reservaModel import Reserva
from django.contrib.auth.models import User


# Consumos adicionales
class ConsumoAdicional(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
