import requests
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
from brandpulsar.utils.helpers import check_domain_txt_records
from main.models import Plan, Domain


@periodic_task(run_every=crontab(minute=0, hour='3'))
def check_domain_redirect():
    # Checks "waiting" domain redirection statuses every day.
    domains = Domain.objects.filter(is_active="waiting")
    for domain in domains:
        result = check_domain_txt_records(domain=domain)
        if result:
            domain.is_active = "pending"
            domain.save()