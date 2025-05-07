from django.urls import path
from . import views

urlpatterns = [
    path("", views.panel_principal, name="panel_principal"),  # Página principal
    path(
        "registro_usuario/", views.registro_usuario, name="registro_usuario"
    ),  # Registro de usuario
    path(
        "iniciar_sesion/", views.iniciar_sesion, name="iniciar_sesion"
    ),  # Iniciar sesión
    path("cerrar_sesion/", views.cerrar_sesion, name="cerrar_sesion"),  # Cerrar sesión
    path(
        "panel_de_usuario/", views.panel_de_usuario, name="panel_de_usuario"
    ),  # Panel de usuario
]
