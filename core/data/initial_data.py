"""Initial Data for the application."""
import json
import logging
from pathlib import Path

from django.db import transaction

from item.models import Unit
from label.models import LabelSheet
from location.models import Room


def read_json_file(file_name):
    data_folder = Path(__file__).parent
    with open(data_folder / file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def recreate_room_table():
    """recreate the Location.Room table."""

    try:
        with transaction.atomic():
            # Delete all records in Room table
            Room.objects.all().delete()
            logging.info("Room table dropped.")
            # Bulk create new records
            Room.objects.bulk_create([Room(name=name) for name in read_json_file("room_names.json")])
            logging.info("Room table recreated.")
    except Exception as e:
        logging.critical("Error recreating Room table: %s", e)


def recreate_unit_table():
    """Recreate the Unit table."""
    units = [Unit(id=i + 1, symbol=symbol) for i, symbol in enumerate(read_json_file("unit_symbols.json"))]

    try:
        with transaction.atomic():
            # Delete all records in Unit table
            Unit.objects.all().delete()
            logging.info("Unit table dropped.")
            # Bulk create new records
            Unit.objects.bulk_create(units)
            logging.info("Unit table recreated.")

    except Exception as e:
        logging.critical("Error recreating Unit table: %s", e)


def create_label_sheet():
    """Create a label sheet."""

    try:
        with transaction.atomic():
            # Delete all records in Unit table
            LabelSheet.objects.all().delete()
            logging.info("Label sheet table dropped.")

            # Bulk create new records
            LabelSheet.objects.bulk_create([LabelSheet(**sheet) for sheet in read_json_file("label_sheets.json")])
            logging.info("Label sheets created.")

    except Exception as e:
        logging.critical("Error recreating Label sheet table: %s", e)
