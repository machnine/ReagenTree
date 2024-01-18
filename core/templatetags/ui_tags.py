"""Template tags for UI elements"""
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def toggle_icon(trigger_id, container_class, icon_class="bi bi-tools text-gray-500", title="Toggle icons", anchor_class="btn btn-sm"):
    """Return a toggle icon for the stock entry requires toggleToolTrayIcons() function in javascript"""
    return format_html(
        '<a href="javascript:" id="{}" class="{}" title="{}" onclick="toggleToolTrayIcons(\'{}\', \'.{}\')">'
        '<i class="{}"></i>'
        "</a>",
        trigger_id,
        anchor_class,
        title,
        trigger_id,
        container_class,
        icon_class,
    )
