from django import forms
from habitaciones.models.consumosAdicionalesModelo import ConsumoAdicional


class ConsumoAdicionalForm(forms.ModelForm):
    class Meta:
        model = ConsumoAdicional
        fields = ["reserva", "usuario", "descripcion", "cantidad", "precio_unitario"]
        widgets = {
            "descripcion": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Detalle del consumo o servicio"}
            ),
            "cantidad": forms.NumberInput(attrs={"min": 1}),
            "precio_unitario": forms.NumberInput(attrs={"step": "0.01"}),
        }
        labels = {
            "reserva": "Reserva asociada",
            "usuario": "Registrado por",
            "descripcion": "Descripción del consumo",
            "cantidad": "Cantidad",
            "precio_unitario": "Precio Unitario",
        }
