import django_filters
from habitaciones.models.models import Habitacion


# Filtros para la clase Habitación
# Se utiliza django_filters para crear filtros personalizados
# para los campos de la clase Habitacion
# Se define la clase HabitacionFilter que hereda de django_filters.FilterSet
class HabitacionFilter(django_filters.FilterSet):
    numero = django_filters.CharFilter(lookup_expr="")
    tipo = django_filters.CharFilter(lookup_expr="")
    capacidad = django_filters.NumberFilter(lookup_expr="")
    descripcion = django_filters.CharFilter(lookup_expr="")

    class Meta:
        model = Habitacion
        fields = ["numero", "tipo", "capacidad", "descripcion"]
