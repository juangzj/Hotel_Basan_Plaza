from django.db import models
from habitaciones.models.models import Habitacion
from django.contrib.auth.models import User
from clientes.models import Cliente
from habitaciones.models.tarifasModelo import Tarifa  # Importar el modelo Tarifa
from django.utils import timezone


# Reservas
class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    tarifa = models.ForeignKey(Tarifa, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    precio_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    pagado = models.BooleanField(default=False)

    @staticmethod
    def obtener_reserva_activa(habitacion_id):
        ahora = timezone.now()
        return Reserva.objects.filter(  # pylint: disable=no-member
            habitacion_id=habitacion_id, fecha_inicio__lte=ahora, fecha_fin__gte=ahora
        ).first()

    def save(self, *args, **kwargs):
        # Cambiar estado de la habitación a 'reservada'
        self.habitacion.estado = "reservada"
        self.habitacion.save()  # pylint: disable=no-member

        # Guardar la reserva normalmente
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de la habitación {self.habitacion.numero} para {self.cliente.nombre} {self.cliente.apellido}"  # pylint: disable=no-member
