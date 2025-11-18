#!/bin/sh

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8080