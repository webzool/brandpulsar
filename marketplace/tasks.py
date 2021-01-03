import json
import requests

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from celery import shared_task

from brandpulsar.utils.helpers import check_domain_txt_records
from marketplace.models import EstimatedDomainPrice


@shared_task
def get_godaddy_estimation(domain):
    url = f'https://uk.godaddy.com/domain-value-appraisal/appraisal/?checkAvail=1&tmskey=&domainToCheck={domain}'
    session = HTMLSession()
    resp = session.get(url)
    resp.html.render(timeout=20)

    soup = BeautifulSoup(resp.html.html, "lxml")
    price = soup.find("span", {"class": "price"}).text
    resp.close()
    session.close()

    domain = EstimatedDomainPrice.objects.create(domain=domain, price=price)
    return domain