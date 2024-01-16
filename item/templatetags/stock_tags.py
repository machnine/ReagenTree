"""Template tags for Stock"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# delivery condition texts
CONDITION_TEXT = {0: "Unknown", 1: "Good", 2: "Unacceptable", 3: "Requires Attention!"}

# delivery condition icons
CONDITION_ICONS = {
    0: "bi-question-diamond text-secondary",
    1: "bi-hand-thumbs-up text-success",
    2: "bi-hand-thumbs-down-fill text-danger",
    3: "bi-exclamation-diamond text-warning",
}


@register.simple_tag
def delivery_condition(condition: int, show_text: bool = False):
    """Return a coloured Bootstrap icon for delivery condition"""

    condition_text = CONDITION_TEXT.get(condition, "") if show_text else ""
    tooltip = f'data-bs-toggle="tooltip" title="Condition: {CONDITION_TEXT.get(condition, "Unknown")}" '
    icons_template = (
        f'<i class="bi {CONDITION_ICONS.get(condition, CONDITION_ICONS[0])}" {tooltip}></i> {condition_text}'
    )
    return mark_safe(icons_template)


# validation status icons

VALIDATION_ICONS = {
    "PENDING": "bi-question text-muted",
    "APPROVED": "bi-circle-fill validation-text-color small",
    "REJECTED": "bi-x-lg text-danger",
    "NOT_REQUIRED": "bi-ban text-gray-300",
}


@register.simple_tag
def validation_status(status: str, show_text: bool = False):
    """Return a coloured Bootstrap icon for validation status"""
    status_text = status if show_text else ""
    status_tooltip = f"""data-bs-toggle="tooltip" title="Status: {status}" """
    icons_template = (
        f'<i class="bi {VALIDATION_ICONS.get(status, VALIDATION_ICONS["PENDING"])}" {status_tooltip}></i> {status_text}'
    )
    return mark_safe(icons_template)


# stock entry colour collections
STOCK_ENTRY_COLOURS = ["stock", "user", "green20", "fushia", "setting", "delivery"]


@register.simple_tag
def stock_entry_colour(ordinal_number: int):
    """Return a colour for the stock entry"""
    index = ordinal_number - 1
    return STOCK_ENTRY_COLOURS[index % len(STOCK_ENTRY_COLOURS)]
