#!/bin/sh
python manage.py makemigrations rest
python manage.py migrate
python manage.py runserver $1
