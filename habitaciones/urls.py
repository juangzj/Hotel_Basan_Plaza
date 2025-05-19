from django.urls import path
from . import views

urlpatterns = [
    path(
        "vista_reservas/", views.vista_reservas, name="vista_reservas"
    ),  # url para ver reservas
    path(
        "ver_cuenta/<int:habitacion_id>/", views.ver_cuenta, name="ver_cuenta"
    ),  # url para ver cuenta
    path(
        "realizar_reserva/", views.realizar_reserva, name="realizar_reserva"
    ),  # url para realizar reserva
    path(
        "crear_consumo_habitacion/<int:habitacion_id>/",
        views.crear_consumo_por_habitacion,
        name="crear_consumo_habitacion",
    ),  # url para crear consumo por habitacion
    path(
        "generar_pdf_cuenta/<int:habitacion_id>/",
        views.generar_pdf_cuenta,
        name="generar_pdf_cuenta",
    ),  # url para generar pdf de cuenta
    path(
        "realizar_cobro/<int:habitacion_id>/",
        views.realizar_cobro,
        name="realizar_cobro",
    ),  # url para realizar cobro
    path(
        "ver_consumos/<int:reserva_id>/",
        views.vista_consumos_adicionales,
        name="ver_consumos",
    ),  # url para ver consumos
    path(
        "eliminar_consumo/<int:consumo_id>/",
        views.eliminar_consumo,
        name="eliminar_consumo",
    ),  # url para eliminar consumo
    path(
        "editar_consumo/<int:consumo_id>/",
        views.editar_consumo,
        name="editar_consumo",
    ),  # url para editar consumo
    path(
        "historial_reservas/", views.historial_reservas, name="historial_reservas"
    ),  # url para historial de reservas
    path(
        "eliminar_reserva/<int:reserva_id>/",
        views.eliminar_reserva,
        name="eliminar_reserva",
    ),  # url para eliminar reserva
    path(
        "editar_reserva/<int:reserva_id>/", views.editar_reserva, name="editar_reserva"
    ),  # url para editar reserva
]
