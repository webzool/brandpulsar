import requests
import dns.resolver
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from main.models import Domain
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


User = get_user_model()


def send_mail_helper(
    subject,
    type=1,
    template='emails/default.html',
    text_message=None,
    html_message=None):

    email_from = settings.EMAIL_FROM
    recipient_list = [html_message.get("email"),]
    if type == 1:
        recipient_list = [
            email_from,
            'info@brandpulsar.com',
            'elmar@webzool.com',
            'mardan@webzool.com'
        ]
    html_message = render_to_string(template, html_message)
    send_mail(
        subject=subject,
        message=text_message,
        from_email=email_from,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False
    )

def check_domain_txt_records(domain):
    """ TODO: refactor """
    kw = 'brandpulsar-verification'
    queries = dns.resolver.query(domain, 'TXT')
    for txt in queries:
        print(txt)
        if kw in str(txt):
            return True
            break
    return False