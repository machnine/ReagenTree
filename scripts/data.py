"""Initial Data for the application."""
from django.db import transaction
from django.db.models import ProtectedError

from item.models import Unit
from label.models import LabelSheet


def recreate_unit_table():
    """Recreate the Unit table."""
    symbols = ["tests", "μl", "ml", "dl", "L", "μg", "mg", "g", "kg"]
    units = [Unit(id=i + 1, symbol=symbol) for i, symbol in enumerate(symbols)]

    try:
        with transaction.atomic():
            # Delete all records in Unit table
            Unit.objects.all().delete()
            print("Unit table dropped.")
            # Bulk create new records
            Unit.objects.bulk_create(units)
            print("Unit table recreated.")

    except ProtectedError as e:
        print(f"Error recreating Unit table: {e}")


def create_label_sheet():
    """Create a label sheet."""

    sheets = [
        {
            "name": "Renal Label",
            "page_size": "A4",
            "label_width": 30,
            "label_height": 26,
            "label_rows": 10,
            "label_cols": 6,
            "margin_left": 8,
            "margin_right": 7,
            "margin_top": 4,
            "margin_bottom": 7,
            "space_x": 3,
            "space_y": 3,
        },
        {
            "name": "Avery L7162",
            "page_size": "A4",
            "label_width": 99.1,
            "label_height": 33.9,
            "label_rows": 8,
            "label_cols": 2,
            "margin_left": 5,
            "margin_right": 5,
            "margin_top": 13,
            "margin_bottom": 13,
            "space_x": 2.5,
            "space_y": 0,
        },
    ]

    try:
        with transaction.atomic():
            # Delete all records in Unit table
            LabelSheet.objects.all().delete()
            print("Label sheet table dropped.")

            # Bulk create new records
            LabelSheet.objects.bulk_create([LabelSheet(**sheet) for sheet in sheets])
            print("Label sheets created.")

    except ProtectedError as e:
        print(f"Error recreating Label sheet table: {e}")


def run():
    """Run the script."""
    recreate_unit_table()
    create_label_sheet()
