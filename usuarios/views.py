from django.shortcuts import (
    render,
    redirect,
)  # Importar render y redirect para manejar vistas
from .forms.UsuarioForm import UserForm  # Importar el formulario de usuario
from .forms.InicioSesionForm import (
    InicioSesionForm,
)  # Importar el formulario de inicio de sesión
from django.contrib import (
    messages,
)  # Importar mensajes para mostrar notificaciones al usuario
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)  # Importar funciones de autenticación
from django.contrib.auth.decorators import (
    login_required,
)  # Importar decorador para requerir autenticación
from habitaciones.models.models import Habitacion  # Importar el modelo de habitación
from habitaciones.filters.filtrosHabitacion import (
    HabitacionFilter,
)  # Importar el filtro de habitaciones


# Metodo para renderizar la vista de inicio
def panel_principal(request):
    return render(request, "panel_principal.html")


# Metodo para renderizar la vista de inicio de sesion
def iniciar_sesion(request):
    if request.method == "POST":
        form = InicioSesionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect("panel_de_usuario")
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")

    else:
        form = InicioSesionForm()

    return render(request, "iniciar_sesion.html", {"form": form})


# Metodo para renderizar la vista de panel de usuario
# Decorador para requerir autenticación en la vista de panel de usuario
@login_required(login_url="iniciar_sesion")
def panel_de_usuario(request):
    # Verificamos si el usuario está autenticado
    if request.user.is_authenticated:
        habitacion_filter = HabitacionFilter(
            request.GET, queryset=Habitacion.objects.all()  # pylint: disable=E1101
        )
        context = {
            "habitacionesForm": habitacion_filter.form,  # Pasamos las habitaciones filtradas al contexto
            "habitacion": habitacion_filter.qs,  # Pasamos el filtro al contexto
        }
        return render(request, "panel_de_usuario.html", context)
    else:
        # Si el usuario no está autenticado, redirigimos a la página de inicio de sesión
        messages.error(request, "Debes iniciar sesión para acceder a esta página")
        return redirect("iniciar_sesion")


#  Metodo para renderizar la vista de cerrar sesion
def cerrar_sesion(request):
    logout(request)  # Cerrar sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect(iniciar_sesion)


# Metodo para renderizar la vista de registro de usuario
def registro_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        # Verificamos si el formulario es válido
        if form.is_valid():
            try:
                user = form.save(commit=False)
                # Encriptamos la contraseña antes de guardar
                user.set_password(form.cleaned_data["password"])
                user.save()
                messages.success(request, "Usuario registrado correctamente.")
                return redirect("panel_de_usuario")
            except Exception as e:
                messages.error(request, f"Ocurrió un error al guardar el usuario: {e}")
        else:
            # Mostramos los errores de validación del formulario
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en {campo}: {error}")
    else:
        # Si la petición no es POST, se muestra el formulario vacío
        form = UserForm()

    # Renderizamos la plantilla con el formulario
    return render(request, "registro_usuario.html", {"form": form})
