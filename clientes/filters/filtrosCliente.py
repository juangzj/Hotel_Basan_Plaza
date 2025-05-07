import django_filters
from clientes.models.clientesModelo import Cliente


#  Filtros para el modelo Cliente
#  Se utiliza django_filters para crear filtros personalizados para el modelo Cliente
#  Se definen filtros para los campos id, nombre, apellido, email, celular y numero_documento
class ClienteFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr="icontains")
    nombre = django_filters.CharFilter(lookup_expr="icontains")
    apellido = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    celular = django_filters.CharFilter(lookup_expr="icontains")
    numero_documento = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Cliente
        fields = ["nombre", "apellido", "email", "celular", "numero_documento"]
