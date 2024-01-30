#!/bin/sh

# Apply database migrations
python manage.py migrate

# Run database initialization script
python manage.py initial_data
# Collect static files
python manage.py collectstatic --noinput
