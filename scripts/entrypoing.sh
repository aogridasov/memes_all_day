#!/bin/bash
set -e

redis-server --daemonize yes

python src/manage.py test src

python src/manage.py migrate --no-input
python src/manage.py collectstatic --no-input
gunicorn --bind 0.0.0.0:8000 --chdir src core.wsgi:application --workers 2 --timeout 300 &

celery --workdir src -A core worker -l info &
celery --workdir src -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
