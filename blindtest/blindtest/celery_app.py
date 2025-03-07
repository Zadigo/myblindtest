import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# celery -A blindtest.celery_app worker -E
# Windows: celery -A blindtest.celery_app worker -E --pool=solo
# celery -A blindtest.celery_app beat -l INFO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blindtest.settings')


def get_broker():
    from django.conf import settings
    return getattr(settings, 'CELERY_BROKER_URL')


def get_backend():
    from django.conf import settings
    return getattr(settings, 'CELERY_RESULT_BACKEND')


app = Celery(
    'myblindtest',
    broker=get_broker(),
    backend=get_backend(),
    logger='celery_app.log'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def monthly_spotify_statistics():
    return {}


@app.task(bind=True)
def billboard_data():
    return {}


@app.task(bind=True)
def get_spotify_data():
    return {}


app.conf.beat_schedule = {
    'monthly-spotify-statistics': {
        'task': 'monthly_spotify_statistics',
        'schedule': crontab(minute='0,3')
    }
}
