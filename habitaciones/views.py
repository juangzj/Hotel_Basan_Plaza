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
from habitaciones.models.consumosAdicionalesModelo import ConsumoAdicional
from django.contrib import messages


@login_required(login_url="iniciar_sesion")
def vista_reservas(request):
    reservas = Reserva.objects.all()  # pylint: disable=no-member
    return render(request, "vista_reservas.html", {"reservas": reservas})


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
    try:
        # Buscar la reserva activa usando el método del modelo
        reserva = Reserva.obtener_reserva_activa(habitacion_id)

        if not reserva:
            messages.error(request, "No hay una reserva activa para esta habitación.")
            return redirect("panel_de_usuario")

        if request.method == "POST":
            form = ConsumoAdicionalForm(request.POST)
            if form.is_valid():
                consumo = form.save(commit=False)
                consumo.reserva = reserva
                consumo.usuario = request.user
                consumo.save()

                messages.success(request, "Consumo adicional agregado correctamente.")
                return redirect("panel_de_usuario")
            else:
                messages.error(request, "Por favor corrige los errores del formulario.")
        else:
            initial_data = {
                "reserva": reserva,
                "usuario": request.user,
            }
            form = ConsumoAdicionalForm(initial=initial_data)

        return render(
            request, "agregar_consumo.html", {"form": form, "reserva": reserva}
        )

    except Exception as e:
        messages.error(request, f"Ocurrió un error inesperado: {str(e)}")
        return redirect("panel_de_usuario")


@login_required(login_url="iniciar_sesion")
def ver_cuenta(request, habitacion_id):
    try:
        hoy = timezone.now()

        # Buscar la reserva activa con pagado = False
        reserva = Reserva.objects.filter(
            habitacion_id=habitacion_id,
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy,
            pagado=False,
        ).first()

        if not reserva:
            messages.error(
                request,
                "No hay una reserva activa pendiente de pago para esta habitación.",
            )
            return redirect("panel_de_usuario")

        # Calcular noches
        noches = (reserva.fecha_fin.date() - reserva.fecha_inicio.date()).days

        # Valor del hospedaje
        valor_hospedaje = (
            reserva.tarifa.precio_por_noche * noches if reserva.tarifa else 0
        )

        # Consumos adicionales
        consumos = ConsumoAdicional.objects.filter(reserva=reserva)

        # Consumos adicionales con total calculado
        consumos_con_total = [
            {
                "descripcion": consumo.descripcion,
                "cantidad": consumo.cantidad,
                "precio_unitario": consumo.precio_unitario,
                "total": consumo.precio_unitario * consumo.cantidad,
            }
            for consumo in consumos
        ]

        # Total consumos
        total_consumos = sum(consumo["total"] for consumo in consumos_con_total)

        # Total general
        total_general = valor_hospedaje + total_consumos

        # Actualizar el precio total de la reserva
        reserva.precio_total = total_general
        reserva.save()

        contexto = {
            "reserva": reserva,
            "valor_hospedaje": valor_hospedaje,
            "consumos": consumos_con_total,
            "total_consumos": total_consumos,
            "total_general": total_general,
        }

        return render(request, "ver_cuenta.html", contexto)

    except Exception as e:
        messages.error(request, f"Ocurrió un error inesperado: {str(e)}")
        return redirect("panel_de_usuario")
