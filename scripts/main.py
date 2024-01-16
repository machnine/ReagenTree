from .data import run as data_run
from .dev import run as dev_run


def run():
    """Create initial data."""
    data_run()
    dev_run()
    print("Initial dev data created.")
