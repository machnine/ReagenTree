"""define inhouse reagent model and it's associated helper models"""
from django.conf import settings
from django.db import models


from item.models import Item


class InhouseReagent(models.Model):
    """Inhouse reagent model"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    components = models.ManyToManyField(
        Item, through="ReagentComponent", related_name="inhouse_reagents"
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_inhouse_reagents",
    )
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_inhouse_reagents",
    )

    def __str__(self):
        """Return string representation of the object"""
        return self.name


class ReagentComponent(models.Model):
    """Inhouse reagent component model"""

    reagent = models.ForeignKey(InhouseReagent, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=1)
    qunatity_unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, null=True)
