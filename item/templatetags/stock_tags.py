"""Template tags for Stock"""
from datetime import date, datetime, timedelta

from django import template
from django.utils import timezone
from django.utils.html import format_html

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
    return format_html(icons_template)


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
    status_tooltip = f"""data-bs-toggle="tooltip" title="Validation status: {status}" """
    icons_template = (
        f'<i class="bi {VALIDATION_ICONS.get(status, VALIDATION_ICONS["PENDING"])}" {status_tooltip}></i> {status_text}'
    )
    return format_html(icons_template)


# stock entry colour collections
STOCK_ENTRY_COLOURS = ["stock", "user", "green20", "fushia", "setting", "delivery"]


@register.simple_tag
def stock_entry_colour(ordinal_number: int):
    """Return a colour for the stock entry"""
    index = ordinal_number - 1
    return STOCK_ENTRY_COLOURS[index % len(STOCK_ENTRY_COLOURS)]


@register.filter(name="expiry_color")
def expiry_color(expiry_date):
    """Return a colour for the expiry date"""
    if isinstance(expiry_date, datetime):
        expiry_date = expiry_date.date()
    if isinstance(expiry_date, date):
        if expiry_date <= timezone.now().date():
            return "text-danger fw-bold"
        if expiry_date <= (timezone.now() + timedelta(days=30)).date():
            return "text-warning fw-bold"
    return "text-primary"


@register.filter(name="watchlist_icon")
def watchlist_icon(watchlist):
    """Return a coloured Bootstrap icon for watchlist"""
    if watchlist:
        return format_html('<i class="bi bi-eye stock-text-color"></i>')
    return ""
