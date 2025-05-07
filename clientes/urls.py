from django.urls import path
from . import views  # Importar las vistas del módulo actual

urlpatterns = [
    path("clientes/", views.vista_clientes, name="vista_clientes"),  # Vista de clientes
    path("crear_cliente/", views.crear_cliente, name="crear_cliente"),  # Crear cliente
    path("ver_cliente/<int:cliente_id>/", views.ver_cliente, name="ver_cliente"),
    path(
        "editar_cliente/<int:cliente_id>/", views.editar_cliente, name="editar_cliente"
    ),
    path(
        "eliminar_cliente/<int:cliente_id>/",
        views.eliminar_cliente,
        name="eliminar_cliente",
    ),
]
