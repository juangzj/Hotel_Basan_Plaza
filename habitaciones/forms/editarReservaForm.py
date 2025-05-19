from django import forms
from habitaciones.models.reservaModel import Reserva


class EditarReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["fecha_inicio", "fecha_fin"]
        widgets = {
            "fecha_inicio": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "fecha_fin": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }
