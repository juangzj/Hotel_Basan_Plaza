from django import template

register = template.Library()


@register.filter
def formatear_pesos(valor):
    try:
        valor = float(valor)
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return valor
