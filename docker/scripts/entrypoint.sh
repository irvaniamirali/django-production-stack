#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
python /wait_for_db.py

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ "$DJANGO_DEBUG" = "0" ]; then
    echo "Starting Gunicorn..."
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --threads 2 \
        --worker-class gthread \
        --worker-tmp-dir /dev/shm \
        --log-level info \
        --access-logfile -
else
    echo "Starting Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
fi
