from django.urls import path
from . import views

urlpatterns = [
    path("", views.panel_principal, name="panel_principal"),
    path("registro_usuario/", views.registro_usuario, name="registro_usuario"),
    path("iniciar_sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("cerrar_sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("panel_de_usuario/", views.panel_de_usuario, name="panel_de_usuario"),
]
