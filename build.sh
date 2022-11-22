#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
pip install 'whitenoise[brotli]'

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --no-input
