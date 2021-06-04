from django import template

register = template.Library()


@register.simple_tag
def get_unread():
    return 3
