from django import template

register = template.Library()


@register.simple_tag
def has_permission(permission_list, allowed_permissions):
    permission_list = set(permission_list.split(","))
    allowed_permissions = set(allowed_permissions)
    if permission_list.issubset(allowed_permissions):
        return True
    return False
