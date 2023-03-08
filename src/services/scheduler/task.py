from celery import Celery
from celery.schedules import crontab

_broker_url='redis://localhost:6379/0'
_backend_url='redis://localhost:6379/0'

def bootstrapScheduler(broker_url=_broker_url, backend_url=_backend_url):
    app = Celery()
    app.conf.broker_url = broker_url
    app.conf.result_backend = broker_url

    return app