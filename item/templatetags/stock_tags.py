"""Template tags for StockItem"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def delivery_condicon(condition):
    """Return a coloured Bootstrap icon for delivery condition"""
    icons = {
        0: mark_safe(
            '<i class="bi bi-question-diamond text-secondary" title="Condition: Unknown"></i>'
        ),
        1: mark_safe('<i class="bi bi-hand-thumbs-up text-success" title="Condition: Good"></i>'),
        2: mark_safe(
            '<i class="bi bi-hand-thumbs-down-fill text-danger" title="Condition: Unacceptable"></i>'
        ),
        3: mark_safe(
            '<i class="bi bi-exclamation-diamond text-warning" title="Condition: Attention required!"></i>'
        ),
    }
    return icons.get(condition, icons[0])
