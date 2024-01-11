""" This file contains the models for the label app. """
from django.db import models


class LabelSheet(models.Model):
    """This model represents a label sheet."""

    name = models.CharField(max_length=50)
    page_size = models.CharField(
        choices=[("A3", "A3"), ("A4", "A4"), ("A5", "A5"), ("LETTER", "LETTER")],
        max_length=10,
    )
    label_width = models.FloatField()
    label_height = models.FloatField()
    label_rows = models.PositiveSmallIntegerField()
    label_cols = models.PositiveSmallIntegerField()
    margin_left = models.FloatField()
    margin_right = models.FloatField()
    margin_top = models.FloatField()
    margin_bottom = models.FloatField()
    space_x = models.FloatField()
    space_y = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.page_size})"

    @property
    def labels_per_sheet(self):
        """Returns the number of labels per sheet."""
        return self.label_rows * self.label_cols
