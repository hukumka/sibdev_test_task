#!/bin/sh
python manage.py makemigrations rest
python manage.py migrate
python -u manage.py runserver $1
