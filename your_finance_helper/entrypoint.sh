#! /bin/bash

python manage.py migrations --no-input

python manage.py migrate --no-input

python manage.py runserver 0.0.0.0:5432