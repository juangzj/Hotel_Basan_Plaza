from django.contrib import admin
from habitaciones.models.models import Habitacion

# Registramos el modelo Habitacion en el admin de Django
admin.site.register(Habitacion)
