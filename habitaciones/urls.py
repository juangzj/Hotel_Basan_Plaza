from django.urls import path
from . import views

urlpatterns = [
    path("vista_reservas/", views.vista_reservas, name="vista_reservas"),
    path("ver_cuenta/<int:id>/", views.ver_cuenta, name="ver_cuenta"),
    path("realizar_reserva/", views.realizar_reserva, name="realizar_reserva"),
]
