from django.db import models


# Este es el modelo de cliente, que representa a un cliente en la base de datos.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=15, unique=True)
    numero_documento = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
