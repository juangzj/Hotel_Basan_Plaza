from django.contrib import admin
from habitaciones.models.models import Habitacion
from habitaciones.models.tarifasModelo import Tarifa
from habitaciones.models.reservaModel import Reserva

# Registramos el modelo Habitacion en el admin de Django
admin.site.register(Habitacion)

# Registramos el modelo Tarifa en el admin de Django
admin.site.register(Tarifa)

# Registramos el modelo Reserva en el admin de Django
admin.site.register(Reserva)
