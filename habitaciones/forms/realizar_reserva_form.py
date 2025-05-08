from django import forms
from habitaciones.models.reservaModel import Reserva


class RealizarReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            "cliente",
            "habitacion",
            "tarifa",
            "usuario",
            "fecha_inicio",
            "fecha_fin",
        ]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "habitacion": forms.HiddenInput(),
            "tarifa": forms.Select(attrs={"class": "form-control"}),
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
        self.fields["habitacion"].disabled = False
        self.fields["usuario"].disabled = False
