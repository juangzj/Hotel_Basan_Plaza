from habitaciones.models.reservaModel import Reserva  # Importar el modelo Reserva
from django.shortcuts import (
    render,
    redirect,
)  # Importar render y redirect para manejar vistas
from django.contrib.auth.decorators import (
    login_required,
)  # Importar decorador para requerir autenticación
from django.shortcuts import render, get_object_or_404
from habitaciones.forms.realizar_reserva_form import RealizarReservaForm
from habitaciones.models.models import Habitacion
from habitaciones.forms.agregarConsumoAdicional import ConsumoAdicionalForm
from django.http import Http404
from django.utils import timezone


@login_required(login_url="iniciar_sesion")
def vista_reservas(request):
    reservas = Reserva.objects.all()  # pylint: disable=no-member
    return render(request, "vista_reservas.html", {"reservas": reservas})


@login_required(login_url="iniciar_sesion")
def ver_cuenta(request, id):
    reserva = get_object_or_404(Reserva, id=id)  # Obtén la reserva usando el id
    return render(request, "ver_cuenta.html", {"reserva": reserva})


@login_required(login_url="iniciar_sesion")
def realizar_reserva(request):
    habitacion_id = request.GET.get("habitacion_id")
    if not habitacion_id:
        return redirect("vista_reservas")

    habitacion = get_object_or_404(Habitacion, id=habitacion_id)

    if request.method == "POST":
        form = RealizarReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.habitacion = habitacion
            reserva.save()

            # Cambiar estado de la habitación
            habitacion.estado = "reservada"
            habitacion.save()

            return redirect("vista_reservas")
    else:
        form = RealizarReservaForm(
            initial={"habitacion": habitacion, "usuario": request.user}
        )

    return render(
        request, "realizar_reserva.html", {"form": form, "habitacion": habitacion}
    )


@login_required(login_url="iniciar_sesion")
def crear_consumo_por_habitacion(request, habitacion_id):
    hoy = timezone.now().date()

    # Buscar la reserva activa para esta habitación (hoy dentro de las fechas de reserva)
    reserva = Reserva.objects.filter(  # pylint: disable=no-member
        habitacion_id=habitacion_id, fecha_inicio__lte=hoy, fecha_fin__gte=hoy
    ).first()

    if not reserva:
        # Si no hay reserva activa, lanzar error 404
        raise Http404("No hay una reserva activa para esta habitación.")

    if request.method == "POST":
        form = ConsumoAdicionalForm(request.POST)
        if form.is_valid():
            consumo = form.save(commit=False)
            consumo.reserva = reserva
            consumo.usuario = request.user
            consumo.save()
            return redirect("panel_de_usuario")
    else:
        initial_data = {
            "reserva": reserva,
            "usuario": request.user,
        }
        form = ConsumoAdicionalForm(initial=initial_data)

    return render(request, "agregar_consumo.html", {"form": form, "reserva": reserva})
