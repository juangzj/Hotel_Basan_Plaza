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


# Vista para mostrar clientes con filtro
@login_required(login_url="iniciar_sesion")
def vista_clientes(request):
    cliente_filter = ClienteFilter(
        request.GET, queryset=Cliente.objects.all()
    )  # pylint: disable=no-member

    # Paginación
    paginator = Paginator(cliente_filter.qs, 5)  # 5 clientes por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": cliente_filter.form,
        "filter": page_obj,  # Pasamos el paginado, no el queryset completo
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
    if request.method == "POST":
        cliente.delete()
        messages.success(request, "Cliente eliminado con éxito.")
        return redirect("vista_clientes")
    return render(request, "eliminar_cliente.html", {"cliente": cliente})
