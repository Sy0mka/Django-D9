from celery import Celery
from celery.schedules import crontab

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly-digest': {
        'task': 'news.tasks.weekly_digest',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
}