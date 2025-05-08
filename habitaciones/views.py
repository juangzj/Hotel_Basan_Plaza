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


@login_required(login_url="iniciar_sesion")
def vista_reservas(request):
    reservas = Reserva.objects.all()  # pylint: disable=no-member
    return render(request, "vista_reservas.html", {"reservas": reservas})


@login_required(login_url="iniciar_sesion")
def ver_cuenta(request, id):
    reserva = get_object_or_404(Reserva, id=id)  # Obtén la reserva usando el id
    return render(request, "ver_cuenta.html", {"reserva": reserva})


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
