#!/bin/sh

# Make migration
python manage.py makemigrations
python manage.py migrate

# Initialize everything
python manage.py init

# Run server
python manage.py runserver 0.0.0.0:8000
