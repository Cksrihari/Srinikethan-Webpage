#!/bin/bash

# Run collectstatic to gather static files
python manage.py collectstatic --noinput

# Start gunicorn
gunicorn borrowers_portal.wsgi --bind=0.0.0.0:8000 --workers=2 --threads=2 --timeout=300
