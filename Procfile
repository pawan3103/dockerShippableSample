web: DJANGO_SETTINGS_MODULE=config.settings.production gunicorn config.wsgi:application
worker: DJANGO_SETTINGS_MODULE=config.settings.production celery worker --concurrency=1 --app=config --loglevel=info
beat: DJANGO_SETTINGS_MODULE=config.settings.production celery beat --app=config --loglevel=info
