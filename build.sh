#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
pip install 'whitenoise[brotli]'

python manage.py collectstatic --no-input
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@mail.com', 'admin123456')" | python manage.py shell