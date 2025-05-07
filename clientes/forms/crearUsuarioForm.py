from django.forms import ModelForm
from clientes.models.clientesModelo import Cliente


class CrearUsuarioForm(ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nombre",
            "apellido",
            "email",
            "celular",
            "numero_documento",
        ]
