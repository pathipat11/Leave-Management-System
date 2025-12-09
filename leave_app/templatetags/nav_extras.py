from django import template

register = template.Library()

@register.filter
def has_group(user, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()

@register.filter
def add_class(field, css):
    existing_classes = field.field.widget.attrs.get("class", "")
    classes = (existing_classes + " " + css).strip()
    return field.as_widget(attrs={"class": classes})