#!/bin/sh
if [ ! -f "DJANGO_INITIALIZED" ]; then
    python manage.py makemigrations rest \
        && python manage.py migrate \
        && python manage.py collectstatic --no-input --clear \
        && touch DJANGO_INITIALIZED
fi
gunicorn sibdevrest.wsgi -b $1
