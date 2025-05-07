from django.contrib import admin
from clientes.models import Cliente


# Registramos el modelo cliente en el admin de Django
admin.site.register(Cliente)
