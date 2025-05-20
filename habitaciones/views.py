from habitaciones.models.reservaModel import Reserva  # Importar el modelo Reserva
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)  # Importar render y redirect para manejar vistas
from django.contrib.auth.decorators import (
    login_required,
)  # Importar decorador para requerir autenticación
from habitaciones.forms.realizar_reserva_form import RealizarReservaForm
from habitaciones.models.models import Habitacion
from habitaciones.forms.agregarConsumoAdicional import ConsumoAdicionalForm
from django.utils import timezone
from habitaciones.models.consumosAdicionalesModelo import ConsumoAdicional
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.paginator import Paginator
from habitaciones.forms.editarReservaForm import EditarReservaForm
from django.db.models import Q


@login_required(login_url="iniciar_sesion")
def vista_reservas(request):
    # Traer solo las reservas no pagadas
    reservas_lista = Reserva.objects.filter(  # pylint: disable=no-member
        pagado=False
    ).order_by(  # pylint: disable=no-member
        "-fecha_inicio"
    )  # pylint: disable=no-member

    paginator = Paginator(reservas_lista, 10)  # 10 por página
    page_number = request.GET.get("page")
    reservas = paginator.get_page(page_number)

    return render(request, "vista_reservas.html", {"reservas": reservas})


@login_required(login_url="iniciar_sesion")
def realizar_reserva(request):
    habitacion_id = request.GET.get("habitacion_id")
    if not habitacion_id:
        return redirect("vista_reservas")

    habitacion = get_object_or_404(Habitacion, id=habitacion_id)

    if request.method == "POST":
        form = RealizarReservaForm(request.POST)
        # Actualizamos las tarifas ANTES de validar
        form.update_tarifas(habitacion_id)

        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.habitacion = habitacion
            reserva.save()

            habitacion.estado = "reservada"
            habitacion.save()

            return redirect("vista_reservas")
    else:
        form = RealizarReservaForm(initial={"usuario": request.user})
        form.update_tarifas(habitacion_id)

    return render(
        request,
        "realizar_reserva.html",
        {"form": form, "habitacion": habitacion},
    )


# Funcion para agregar un consumo adicional a una reserva
# Se asume que la reserva ya fue creada y está pendiente de pago
# Se debe verificar que la habitación esté ocupada y que la reserva no haya sido pagada


@login_required(login_url="iniciar_sesion")
def crear_consumo_por_habitacion(request, habitacion_id):
    try:
        # Buscar la reserva pendiente de pago (sin importar fechas)
        reserva = Reserva.objects.filter(  # pylint: disable=no-member
            habitacion_id=habitacion_id, pagado=False
        ).first()

        if not reserva:
            messages.error(
                request, "No hay una reserva pendiente de pago para esta habitación."
            )
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


# Funcion para ver la cuenta de la reserva
# Se asume que la reserva ya fue creada y está pendiente de pago
# Se debe verificar que la habitación esté ocupada y que la reserva no haya sido pagada
# Se debe calcular el total a pagar y mostrarlo al usuario
@login_required(login_url="iniciar_sesion")
def ver_cuenta(request, habitacion_id):
    try:
        reserva = Reserva.objects.filter(  # pylint: disable=no-member
            habitacion_id=habitacion_id, pagado=False
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

        consumos = ConsumoAdicional.objects.filter(  # pylint: disable=no-member
            reserva=reserva
        )

        for consumo in consumos:
            consumo.total = consumo.precio_unitario * consumo.cantidad

        total_consumos = sum(consumo.total for consumo in consumos)

        total_general = valor_hospedaje + total_consumos

        reserva.precio_total = total_general
        reserva.save()

        contexto = {
            "reserva": reserva,
            "noches": noches,
            "valor_hospedaje": valor_hospedaje,
            "consumos": consumos,
            "total_consumos": total_consumos,
            "total_general": total_general,
        }

        return render(request, "ver_cuenta.html", contexto)

    except Exception as e:
        messages.error(request, f"Ocurrió un error inesperado: {str(e)}")
        return redirect("panel_de_usuario")


# Funcion para generar el PDF de la cuenta
# Se asume que la reserva ya fue creada y está pendiente de pago
# Se debe verificar que la habitación esté ocupada y que la reserva no haya sido pagada
@login_required(login_url="iniciar_sesion")
def generar_pdf_cuenta(request, habitacion_id):
    try:
        reserva = Reserva.objects.filter(  # pylint: disable=no-member
            habitacion_id=habitacion_id,
            pagado=False,
        ).first()

        if not reserva:
            messages.error(
                request, "No hay una reserva pendiente de pago para esta habitación."
            )
            return redirect("panel_de_usuario")

        noches = (reserva.fecha_fin.date() - reserva.fecha_inicio.date()).days
        valor_hospedaje = (
            reserva.tarifa.precio_por_noche * noches if reserva.tarifa else 0
        )

        consumos = ConsumoAdicional.objects.filter(  # pylint: disable=no-member
            reserva=reserva
        )

        for consumo in consumos:
            consumo.total = consumo.precio_unitario * consumo.cantidad

        total_consumos = sum(consumo.total for consumo in consumos)
        total_general = valor_hospedaje + total_consumos

        reserva.precio_total = total_general
        reserva.save()

        contexto = {
            "reserva": reserva,
            "noches": noches,
            "valor_hospedaje": valor_hospedaje,
            "consumos": consumos,
            "total_consumos": total_consumos,
            "total_general": total_general,
        }

        template = get_template("cuenta_pdf.html")
        html_string = template.render(contexto)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="cuenta_habitacion_{habitacion_id}.pdf"'
        )

        pisa_status = pisa.CreatePDF(html_string, dest=response)

        if pisa_status.err:
            return HttpResponse("Error al generar el PDF")

        return response

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return redirect("panel_de_usuario")


# Funcion para realizar el cobro de la reserva
# Se asume que la reserva ya fue creada y está pendiente de pago
# Se debe verificar que la habitación esté ocupada y que la reserva no haya sido pagada
# Se debe calcular el total a pagar y mostrarlo al usuario
@login_required(login_url="iniciar_sesion")
def realizar_cobro(request, habitacion_id):
    try:
        reserva = Reserva.objects.filter(  # pylint: disable=no-member
            habitacion_id=habitacion_id, pagado=False
        ).first()

        if not reserva:
            messages.error(
                request,
                "No hay una reserva activa pendiente de pago para esta habitación.",
            )
            return redirect("panel_de_usuario")

        # Calcular noches y totales igual que en ver_cuenta
        noches = (reserva.fecha_fin.date() - reserva.fecha_inicio.date()).days
        valor_hospedaje = (
            reserva.tarifa.precio_por_noche * noches if reserva.tarifa else 0
        )

        consumos = ConsumoAdicional.objects.filter(  # pylint: disable=no-member
            reserva=reserva
        )  # pylint: disable=no-member
        for consumo in consumos:
            consumo.total = consumo.precio_unitario * consumo.cantidad

        total_consumos = sum(consumo.total for consumo in consumos)
        total_general = valor_hospedaje + total_consumos

        reserva.precio_total = total_general
        reserva.save()

        if request.method == "POST":
            # Confirmar cobro: marcar pagado y liberar habitación
            reserva.pagado = True
            reserva.save()

            reserva.habitacion.estado = "disponible"
            reserva.habitacion.save()

            messages.success(request, "Reserva cobrada correctamente.")
            return redirect("panel_de_usuario")

        contexto = {
            "reserva": reserva,
            "noches": noches,
            "valor_hospedaje": valor_hospedaje,
            "consumos": consumos,
            "total_consumos": total_consumos,
            "total_general": total_general,
        }

        return render(request, "realizar_cobro.html", contexto)

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return redirect("panel_de_usuario")


# Funciopn para ver los consumos adicionales de una reserva
@login_required(login_url="iniciar_sesion")
def vista_consumos_adicionales(request, reserva_id):
    # Obtener la reserva o error 404
    reserva = get_object_or_404(Reserva, id=reserva_id)

    # Obtener la habitación asociada
    habitacion = reserva.habitacion

    # Obtener consumos asociados a la reserva
    consumos_query = ConsumoAdicional.objects.filter(  # pylint: disable=no-member
        reserva=reserva
    ).order_by("fecha")

    # Calcular total en cada consumo y total general
    consumos = []
    total_general = 0
    for consumo in consumos_query:
        consumo.total = consumo.cantidad * consumo.precio_unitario
        total_general += consumo.total
        consumos.append(consumo)

    # Paginador para consumos
    paginator = Paginator(consumos, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "habitacion": habitacion,
        "reserva": reserva,
        "consumos": page_obj,
        "total_general": total_general,
    }

    return render(request, "vista_consumos.html", context)


# Funcion para eliminar un consumo adicional
@login_required(login_url="iniciar_sesion")
def eliminar_consumo(request, consumo_id):
    consumo = get_object_or_404(ConsumoAdicional, id=consumo_id)
    reserva_id = consumo.reserva.id  # Obtener reserva_id antes de eliminar
    if request.method == "POST":
        consumo.delete()
        messages.success(request, "Consumo eliminado con éxito.")
        return redirect("ver_consumos", reserva_id=reserva_id)
    return render(request, "eliminar_consumo.html", {"consumo": consumo})


# funcion para editar un consumo adicional
@login_required(login_url="iniciar_sesion")
def editar_consumo(request, consumo_id):
    consumo = get_object_or_404(ConsumoAdicional, id=consumo_id)

    if request.method == "POST":
        form = ConsumoAdicionalForm(request.POST, instance=consumo)
        if form.is_valid():
            form.save()
            messages.success(request, "Consumo editado con éxito.")
            return redirect("ver_consumos", reserva_id=consumo.reserva.id)
    else:
        form = ConsumoAdicionalForm(instance=consumo)

    return render(request, "editar_consumo.html", {"form": form, "consumo": consumo})


# Funcion para ver el historial de reservas
@login_required(login_url="iniciar_sesion")
def historial_reservas(request):
    filtros = request.GET.getlist("filtros[]")
    valores = request.GET.getlist("valores[]")

    reservas = Reserva.objects.all().order_by(  # pylint: disable=no-member
        "-fecha_inicio"
    )  # pylint: disable=no-member

    if filtros and valores and len(filtros) == len(valores):
        query = Q()
        for filtro, valor in zip(filtros, valores):
            if filtro == "cliente":
                query &= Q(cliente__nombre__icontains=valor) | Q(
                    cliente__apellido__icontains=valor
                )
            elif filtro == "habitacion":
                query &= Q(habitacion__numero__icontains=valor)
            elif filtro == "usuario":
                query &= Q(usuario__username__icontains=valor)
            elif filtro == "tarifa":
                query &= Q(tarifa__precio_por_noche__icontains=valor)
            elif filtro == "fecha_inicio":
                query &= Q(fecha_inicio__icontains=valor)
            elif filtro == "fecha_fin":
                query &= Q(fecha_fin__icontains=valor)
            elif filtro == "pagado":
                if valor.lower() in ("sí", "si", "true", "1"):
                    query &= Q(pagado=True)
                elif valor.lower() in ("no", "false", "0"):
                    query &= Q(pagado=False)
                else:
                    reservas = (
                        Reserva.objects.none()  # pylint: disable=no-member
                    )  # Invalid value
                    break
        reservas = reservas.filter(query)

    paginator = Paginator(reservas, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "reservas": page_obj,
        "filtros": filtros,
        "valores": valores,
    }
    return render(request, "historial_reservas.html", context)


# Funcion para eliminar una reserva
@login_required(login_url="iniciar_sesion")
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == "POST":
        # Cambiar el estado de la habitación a 'disponible'
        habitacion = reserva.habitacion
        habitacion.estado = "disponible"
        habitacion.save()

        # Eliminar la reserva
        reserva.delete()

        messages.success(request, "Reserva eliminada con éxito")
        return redirect("vista_reservas")

    return render(request, "eliminar_reserva.html", {"reserva": reserva})


# funcion para editar una reserva
@login_required(login_url="iniciar_sesion")
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    if request.method == "POST":
        form = EditarReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva actualizada correctamente.")
            return redirect("vista_reservas")
        else:
            messages.error(request, "Hubo un error al actualizar la reserva.")
    else:
        form = EditarReservaForm(instance=reserva)

    return render(request, "editar_reserva.html", {"form": form, "reserva": reserva})
