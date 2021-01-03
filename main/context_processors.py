from django.conf import settings
from main.models import BlogPost, Faq, Industry


def latest_blogs_processor(request):
    blog_posts = BlogPost.objects.order_by('-date_created')[:5]

    return {'latest_blog_posts': blog_posts}


def allow_bots(request):
    allow = False
    if settings.ALLOW_BOTS:
        allow = True
    return {'allow_bots': allow}


def faqs_processor(request):
    faqs = Faq.objects.all().order_by('-pk')
    buyers = Faq.objects.filter(category='buyer')
    sellers = Faq.objects.filter(category='seller')
    return {'faqs': faqs, 'buyers': buyers, 'sellers': sellers}


def industries_processor(request):
    footer_industries = Industry.objects.order_by('-date_created')
    return {
        'footer_industries': footer_industries
    }
