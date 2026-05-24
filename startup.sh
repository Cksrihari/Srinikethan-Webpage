#!/bin/bash

# Run collectstatic to gather static files
python manage.py collectstatic --noinput

# Start gunicorn
gunicorn srinikethan_website.wsgi --bind=0.0.0.0:8000 --workers=2 --threads=2 --timeout=300
