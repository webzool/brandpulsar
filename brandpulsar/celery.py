from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brandpulsar.settings")

app = Celery("brandpulsar")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


app.conf.beat_schedule = {
    # Core
    "central_bank_get_currencies": {
        "task": "core.tasks.fetch_currency_rates",
        "schedule": crontab(
            minute="15", hour="10", day_of_month="*", month_of_year="*", day_of_week="*"
        ),
    },
    #     # Category
    #     "update_filter_choices": {
    #         "task": "category.tasks.remove_unnecessary_filter_choices",
    #         "schedule": crontab(minute="0", hour="*/1"),
    #     },
}
