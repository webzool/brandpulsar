import requests

from django.conf import settings

def get_domain_appraisal(domain):
    # Godaddy Aprraisal endpoint
    appraisal_endpoint = f"https://api.godaddy.com/v1/appraisal/{domain}"
    # Authorization header details
    headers = {"Authorization": f"sso-key {settings.GODADDY_KEY}:{settings.GODADDY_SECRET}"}
    response = requests.get(
        appraisal_endpoint,
        headers=headers).json()
    return {
        "domain" : domain,
        "estimated_price" : response.get("govalue")
    }
