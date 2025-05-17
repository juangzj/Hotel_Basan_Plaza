import django_filters
from clientes.models.clientesModelo import Cliente


class ClienteFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter()
    nombre = django_filters.CharFilter(lookup_expr="icontains")
    apellido = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    celular = django_filters.CharFilter(lookup_expr="icontains")
    numero_documento = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Cliente
        fields = ["id", "nombre", "apellido", "email", "celular", "numero_documento"]
