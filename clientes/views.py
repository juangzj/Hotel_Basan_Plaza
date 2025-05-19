from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import (
    login_required,
)  # Importar decorador para requerir autenticación
from .filters.filtrosCliente import ClienteFilter  # Importar el filtro de clientes
from .models import Cliente  # Importar el modelo de cliente
from .forms.crearUsuarioForm import (
    CrearUsuarioForm,
)  # Importar el formulario de creación de usuario
from django.contrib import messages  # Importar mensajes para mostrar notificaciones
from django.core.paginator import Paginator
from habitaciones.models.reservaModel import Reserva  # Importar el modelo de reserva


@login_required(login_url="iniciar_sesion")
def vista_clientes(request):
    # Capturamos los valores del formulario GET
    filtro = request.GET.get("filtro")
    valor = request.GET.get("valor")

    clientes = Cliente.objects.all()  # pylint: disable=no-member

    if filtro and valor:
        if filtro == "nombre":
            clientes = clientes.filter(nombre__icontains=valor)
        elif filtro == "apellido":
            clientes = clientes.filter(apellido__icontains=valor)
        elif filtro == "email":
            clientes = clientes.filter(email__icontains=valor)
        elif filtro == "celular":
            clientes = clientes.filter(celular__icontains=valor)
        elif filtro == "numero_documento":
            clientes = clientes.filter(numero_documento__icontains=valor)

    # Paginación (5 clientes por página)
    paginator = Paginator(clientes, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "clientes": page_obj,  # Pasamos el paginado, no todo el queryset
    }

    return render(request, "vista_clientes.html", context)


# Funcion para crear un nuevo cliente
# Esta vista permite a los usuarios crear un nuevo cliente en la base de datos.
@login_required(login_url="iniciar_sesion")
def crear_cliente(request):
    if request.method == "POST":
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            cliente_nuevo = form.save(commit=False)
            cliente_nuevo.save()
            messages.success(request, "Cliente creado con éxito.")
            return redirect("/panel_de_usuario/clientes/")
        else:
            messages.error(request, "El cliente no se pudo crear.")
    else:
        form = CrearUsuarioForm()

    return render(request, "crear_cliente.html", {"form": form})


# Funcion para ver la informacion de un cliente
@login_required(login_url="iniciar_sesion")
def ver_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, "ver_cliente.html", {"cliente": cliente})


# funcion para editar un cliente
@login_required(login_url="iniciar_sesion")
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    form = CrearUsuarioForm(request.POST or None, instance=cliente)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente editado con éxito.")
            return redirect("vista_clientes")
        else:
            messages.error(request, "El cliente no se pudo editar.")
    return render(request, "editar_cliente.html", {"form": form, "cliente": cliente})


# Funcion para eliminar un cliente
@login_required(login_url="iniciar_sesion")
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Verificar si el cliente tiene reservas no pagadas
    reservas_pendientes = Reserva.objects.filter(  # pylint: disable=no-member
        cliente=cliente, pagado=False
    )

    if request.method == "POST":
        if reservas_pendientes.exists():
            messages.error(
                request,
                "No se puede eliminar este cliente porque tiene reservas pendientes de pago.",
            )
            return redirect("vista_clientes")
        else:
            cliente.delete()
            messages.success(request, "Cliente eliminado con éxito.")
            return redirect("vista_clientes")

    return render(request, "eliminar_cliente.html", {"cliente": cliente})
