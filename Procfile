web: gunicorn biblioteca_do_saber.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
worker: celery -A biblioteca_do_saber worker -l info -c 4
beat: celery -A biblioteca_do_saber beat -l info
release: python manage.py migrate --noinput
