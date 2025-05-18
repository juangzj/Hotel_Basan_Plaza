import django_filters
from django import forms
from habitaciones.models.models import Habitacion


class HabitacionFilter(django_filters.FilterSet):
    ESTADO_CHOICES = [
        ("", "---------"),  # Opción vacía para permitir no filtrar
        ("disponible", "Disponible"),
        ("reservada", "Reservada"),
    ]

    numero = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Número de habitación",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: 101"}
        ),
    )
    tipo = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Tipo de habitación",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: Suite"}
        ),
    )
    capacidad = django_filters.NumberFilter(
        lookup_expr="exact",
        label="Capacidad",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Ej: 2"}
        ),
    )
    descripcion = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Descripción",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: Vista al mar"}
        ),
    )
    estado = django_filters.ChoiceFilter(
        choices=ESTADO_CHOICES,
        label="Estado de la habitación",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Habitacion
        fields = ["numero", "tipo", "capacidad", "descripcion", "estado"]
