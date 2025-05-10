from django.urls import path
from . import views

urlpatterns = [
    path("vista_reservas/", views.vista_reservas, name="vista_reservas"),
    path("ver_cuenta/<int:habitacion_id>/", views.ver_cuenta, name="ver_cuenta"),
    path("realizar_reserva/", views.realizar_reserva, name="realizar_reserva"),
    path(
        "crear_consumo_habitacion/<int:habitacion_id>/",
        views.crear_consumo_por_habitacion,
        name="crear_consumo_habitacion",
    ),
    path(
        "generar_pdf_cuenta/<int:habitacion_id>/",
        views.generar_pdf_cuenta,
        name="generar_pdf_cuenta",
    ),
]
