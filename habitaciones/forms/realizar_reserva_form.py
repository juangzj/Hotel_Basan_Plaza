from django import forms
from habitaciones.models.reservaModel import Reserva
from clientes.models.clientesModelo import Cliente
from habitaciones.models.models import Habitacion
from habitaciones.models.tarifasModelo import Tarifa


class RealizarReservaForm(forms.ModelForm):
    cliente = forms.CharField(
        label="Cliente",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Escribe el nombre o documento del cliente",
            }
        ),
    )

    tarifa = forms.ModelChoiceField(
        queryset=Tarifa.objects.none(),  # Inicialmente vacío # pylint: disable=no-member
        label="Tarifa",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Reserva
        fields = [
            "cliente",
            "tarifa",
            "usuario",
            "fecha_inicio",
            "fecha_fin",
        ]
        widgets = {
            "usuario": forms.HiddenInput(),
            "fecha_inicio": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "fecha_fin": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["usuario"].disabled = False

    def clean_cliente(self):
        cliente_input = self.cleaned_data.get("cliente")

        try:
            cliente = Cliente.objects.get(  # pylint: disable=no-member
                numero_documento=cliente_input
            )
        except Cliente.DoesNotExist:  # pylint: disable=no-member
            try:
                cliente = Cliente.objects.get(  # pylint: disable=no-member
                    nombre__icontains=cliente_input
                )
            except Cliente.DoesNotExist:  # pylint: disable=no-member
                raise forms.ValidationError("Cliente no encontrado.")

        return cliente

    def update_tarifas(self, habitacion_id):
        """Actualiza el campo 'tarifa' con las tarifas asociadas a la habitación seleccionada."""
        if habitacion_id:
            tarifas = Tarifa.objects.filter(  # pylint: disable=no-member
                habitacion_id=habitacion_id
            )  # pylint: disable=no-member
            self.fields["tarifa"].queryset = tarifas
        else:
            self.fields["tarifa"].queryset = (
                Tarifa.objects.none()  # pylint: disable=no-member
            )  # pylint: disable=no-member
