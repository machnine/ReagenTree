"""Template tags for Stock"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def delivery_condition(condition: int, show_text: bool = False):
    """Return a coloured Bootstrap icon for delivery condition"""
    condition_texts = {
        0: "Unknown",
        1: "Good",
        2: "Unacceptable",
        3: "Requires Attention!",
    }
    optional_condition_text = condition_texts.get(condition, "") if show_text else ""
    condition_text = condition_texts.get(condition, "Unknown")
    icons = {
        0: mark_safe(
            f'<i class="bi bi-question-diamond text-secondary" data-bs-toggle="tooltip" title="Condition: {condition_text}"></i> {optional_condition_text}'
        ),
        1: mark_safe(
            f'<i class="bi bi-hand-thumbs-up text-success" data-bs-toggle="tooltip" title="Condition: {condition_text}"></i> {optional_condition_text}'
        ),
        2: mark_safe(
            f'<i class="bi bi-hand-thumbs-down-fill text-danger" data-bs-toggle="tooltip" title="Condition: {condition_text}"></i> {optional_condition_text}'
        ),
        3: mark_safe(
            f'<i class="bi bi-exclamation-diamond text-warning" data-bs-toggle="tooltip" title="Condition: {condition_text}"></i> {optional_condition_text}'
        ),
    }
    return icons.get(condition, icons[0])


@register.simple_tag
def validation_status(status: str, show_text: bool = False):
    """Return a coloured Bootstrap icon for validation status"""
    status_text = status if show_text else ""

    icons = {
        "PENDING": mark_safe(
            f'<span class="text-muted"><i class="bi bi-question" data-bs-toggle="tooltip" title="Status: Pending"></i> {status_text}</span>'
        ),
        "APPROVED": mark_safe(
            f'<span class="text-success fw-bold"><i class="bi bi-check-lg" data-bs-toggle="tooltip" title="Status: Approved"></i> {status_text}</span>'
        ),
        "REJECTED": mark_safe(
            f'<span class="text-danger fw-bold"><i class="bi bi-x-lg" data-bs-toggle="tooltip" title="Status: Rejected"></i> {status_text}</span>'
        ),
        "NOT_REQUIRED": mark_safe(
            f'<span class="text-gray-300"><i class="bi bi-ban" data-bs-toggle="tooltip" title="Status: Not required"></i>  {status_text}</span>'
        ),
    }
    return icons.get(status, icons["PENDING"])
