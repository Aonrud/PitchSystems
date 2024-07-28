#!/bin/sh

poetry run python manage.py migrate --noinput
poetry run python manage.py collectstatic --noinput
poetry run python manage.py loaddata fixtures/*.json
poetry run gunicorn pitch_systems_api.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000
