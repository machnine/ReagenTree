""" This file contains the models for the label app. """
from django.db import models


class LabelSheet(models.Model):
    """This model represents a label sheet."""

    name = models.CharField(max_length=50)
    page_size = models.CharField(
        choices=[
            ("A3", "A3"),
            ("A4", "A4"),
            ("A5", "A5"),
            ("LETTER", "LETTER"),
            ("LEGAL", "LEGAL"),
        ],
        max_length=10,
    )
    label_width = models.DecimalField(max_digits=4, decimal_places=1)
    label_height = models.DecimalField(max_digits=4, decimal_places=1)
    label_rows = models.PositiveSmallIntegerField()
    label_cols = models.PositiveSmallIntegerField()
    margin_left = models.DecimalField(max_digits=4, decimal_places=1)
    margin_right = models.DecimalField(max_digits=4, decimal_places=1)
    margin_top = models.DecimalField(max_digits=4, decimal_places=1)
    margin_bottom = models.DecimalField(max_digits=4, decimal_places=1)
    space_x = models.DecimalField(max_digits=4, decimal_places=1)
    space_y = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return f"{self.name} ({self.page_size})"

    @property
    def labels_per_sheet(self):
        """Returns the number of labels per sheet."""
        return self.label_rows * self.label_cols
