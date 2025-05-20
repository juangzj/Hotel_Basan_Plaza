import django_filters
from django import forms
from habitaciones.models.reservaModel import Reserva
from clientes.models import Cliente
from habitaciones.models.models import Habitacion
from habitaciones.models.tarifasModelo import Tarifa
from django.contrib.auth.models import User


class ReservaFilter(django_filters.FilterSet):
    cliente = django_filters.ModelChoiceFilter(
        queryset=Cliente.objects.all(),
        label="Cliente",
        empty_label="Todos",
        widget=forms.Select(attrs={"class": "form-control"}),
        method="filter_cliente_nombre",
        required=False,
    )
    habitacion = django_filters.ModelChoiceFilter(
        queryset=Habitacion.objects.all(),
        label="Habitación",
        empty_label="Todas",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    tarifa = django_filters.ModelChoiceFilter(
        queryset=Tarifa.objects.all(),
        label="Tarifa",
        empty_label="Todas",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    usuario = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Usuario",
        empty_label="Todos",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    pagado = django_filters.ChoiceFilter(
        choices=[("", "---------"), ("True", "Pagado"), ("False", "No pagado")],
        label="Estado de pago",
        widget=forms.Select(attrs={"class": "form-control"}),
        method="filter_pagado",
        required=False,
    )
    fecha_inicio = django_filters.DateFromToRangeFilter(
        label="Rango fecha inicio",
        widget=django_filters.widgets.RangeWidget(
            attrs={"type": "date", "class": "form-control"}
        ),
        required=False,
    )
    fecha_fin = django_filters.DateFromToRangeFilter(
        label="Rango fecha fin",
        widget=django_filters.widgets.RangeWidget(
            attrs={"type": "date", "class": "form-control"}
        ),
        required=False,
    )

    class Meta:
        model = Reserva
        fields = [
            "cliente",
            "habitacion",
            "tarifa",
            "usuario",
            "pagado",
            "fecha_inicio",
            "fecha_fin",
        ]

    def filter_cliente_nombre(self, queryset, name, value):
        if value:
            return queryset.filter(cliente__nombre__icontains=value.nombre)
        return queryset

    def filter_pagado(self, queryset, name, value):
        if value == "True":
            return queryset.filter(pagado=True)
        elif value == "False":
            return queryset.filter(pagado=False)
        return queryset
