import django_filters
from habitaciones.models.models import Habitacion


# Filtros para la clase Habitación
class HabitacionFilter(django_filters.FilterSet):
    ESTADO_CHOICES = [
        ("disponible", "Disponible"),
        ("reservada", "Reservada"),
    ]

    numero = django_filters.CharFilter(
        lookup_expr="icontains", label="Número de habitación", required=False
    )
    tipo = django_filters.CharFilter(
        lookup_expr="icontains", label="Tipo de habitación", required=False
    )
    capacidad = django_filters.NumberFilter(
        lookup_expr="exact", label="Capacidad", required=False
    )
    descripcion = django_filters.CharFilter(
        lookup_expr="icontains", label="Descripción", required=False
    )
    estado = django_filters.ChoiceFilter(
        choices=ESTADO_CHOICES, label="Estado de la habitación", required=False
    )

    class Meta:
        model = Habitacion
        fields = ["numero", "tipo", "capacidad", "descripcion", "estado"]
