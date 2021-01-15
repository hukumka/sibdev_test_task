#!/bin/sh
python manage.py makemigrations rest
python manage.py migrate
gunicorn sibdevrest.wsgi -b $1
