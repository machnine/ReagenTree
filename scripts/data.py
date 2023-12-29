"""Initial Data for the application."""
from django.db import transaction
from django.db.models import ProtectedError

from item.models import Unit


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


def run():
    """Run the script."""
    recreate_unit_table()