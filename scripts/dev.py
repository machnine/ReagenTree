"""Intial values for development"""
from random import randint

from category.models import Category
from company.models import Company
from item.models import Item, Unit
from location.models import Location
from user.models import CustomUser

inital_users = [
    {
        "username": "admin",
        "password": "password",
        "is_superuser": True,
        "is_active": True,
        "is_staff": True,
        "email": "admin@localhost",
        "first_name": "Admin",
        "last_name": "User",
        "initials": "AU",
    },
    {
        "username": "user",
        "password": "password",
        "is_superuser": False,
        "is_active": True,
        "is_staff": True,
        "email": "user@localhost",
        "first_name": "Normal",
        "last_name": "User",
        "initials": "NU",
    },
    {
        "username": "guest",
        "password": "password",
        "is_superuser": False,
        "is_active": True,
        "is_staff": False,
        "email": "guest@localhost",
        "first_name": "Guest",
        "last_name": "User",
        "initials": "GU",
    },
]


initial_categories = [{"name": f"Category {n}", "description": f"This is Category {n}."} for n in range(1, 21)]
initial_companies = [{"name": f"Company {n}", "description": f"This is Company {n}."} for n in range(1, 21)]
initial_locations = [{"name": f"Location {n}", "description": f"This is Location {n}."} for n in range(1, 21)]

initial_items = [{"name": f"Item {n}", "description": f"This is Item {n}."} for n in range(1, 21)]


def create_initial_categories():
    """Create initial categories."""
    Category.objects.all().delete()
    for category in initial_categories:
        Category.objects.create(**category)


def create_initial_companies():
    """Create initial companies."""
    Company.objects.all().delete()
    for company in initial_companies:
        Company.objects.create(**company)


def create_initial_locations():
    """Create initial locations."""
    Location.objects.all().delete()
    for location in initial_locations:
        Location.objects.create(**location)


def create_initial_items():
    """Create initial items."""
    Item.objects.all().delete()
    for item in initial_items:
        Item.objects.create(
            **item,
            quantity=randint(1, 1000),
            quantity_unit=Unit.objects.get(pk=randint(1, 9)),
            category=Category.objects.get(pk=randint(1, 20)),
            supplier=Company.objects.get(pk=randint(1, 20)),
            manufacturer=Company.objects.get(pk=randint(1, 20)),
            product_id=randint(10000, 99999),
            cas_number=f"{randint(10, 99)}-{randint(100, 999)}-{randint(100, 999)}",
        )


def create_initial_users():
    """Create initial users."""
    CustomUser.objects.all().delete()
    for user in inital_users:
        CustomUser.objects.create_user(**user)


def run():
    """Create initial data."""
    try:
        create_initial_categories()
        create_initial_companies()
        create_initial_locations()
        create_initial_items()
        create_initial_users()
        print("Initial dev data created.")
    except Exception as e:
        print(f"Error creating initial dev data: {e}")
        print("Flush the database and try again: `python manage.py flush`")
