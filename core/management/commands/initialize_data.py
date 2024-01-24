"""Initialize the database with some data"""
from django.core.management.base import BaseCommand

from core.data.initial_data import create_label_sheet, recreate_room_table, recreate_unit_table


class Command(BaseCommand):
    help = "Initialize the database with some data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Initializing data..."))
        recreate_room_table()
        self.stdout.write(self.style.SUCCESS("Room names..."))
        recreate_unit_table()
        self.stdout.write(self.style.SUCCESS("Unit symbols..."))
        create_label_sheet()
        self.stdout.write(self.style.SUCCESS("Label sheets..."))
        self.stdout.write(self.style.SUCCESS("Data initialized successfully!"))
