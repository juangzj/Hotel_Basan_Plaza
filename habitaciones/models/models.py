from django.db import models


# Clase para la tabla de habitaciones
class Habitacion(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    descrpcion = models.TextField()

    def __str__(self):
        return f"Habitacion {self.numero} - {self.tipo}"
