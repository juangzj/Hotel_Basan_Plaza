from django import template

register = template.Library()


@register.filter
def has_key(dict_data, key):
    return key in dict_data


@register.filter
def dict_get(dict_data, key):
    return dict_data.get(key)
