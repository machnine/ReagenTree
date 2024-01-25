#!/bin/sh

# Apply database migrations
python manage.py migrate

# Run database initialization script
python manage.py initial_data
# Collect static files
python manage.py collectstatic --noinput
# Start server
python manage.py runserver 0.0.0.0:8000