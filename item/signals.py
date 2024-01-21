"""Signals for item app."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from item.models import ReagentComponent, Stock, StockValidation


@receiver(post_save, sender=ReagentComponent)
def update_stock_validation_on_component_change(sender, instance, **kwargs):
    """Update an Inhouse Reagent's stock's validation status when a component is added or removed."""
    # parent inhouse reagent
    inhouse_reagent = instance.reagent
    # the stock instances that the inhouse reagent is associated with
    related_stocks = Stock.objects.filter(inhouse_reagent=inhouse_reagent)
    for stock in related_stocks:
        # the stock validation instances associated with the stock
        stock_validations = StockValidation.objects.filter(stock=stock)
        for sv in stock_validations:
            # if the validation status is not pending, set it to pending
            if sv.validation.status != "PENDING":
                sv.validation.status = "PENDING"
                timestamp = timezone.now().strftime("%d/%m/%Y %H:%M:%S")
                message = f"Reagent component(s) changed ({timestamp}) - revalidate stock!"
                sv.validation.comments = message
                sv.validation.save()
