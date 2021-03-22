from django.contrib.sitemaps import Sitemap
from main.models import BlogPost, Domain, BlogCategory, Industry
from django.urls import reverse


class BlogPostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.date_updated


class DomainSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Domain.objects.all()


class IndustrySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Industry.objects.all()


class BlogCategorySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return BlogCategory.objects.all()


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'main:index',
            'main:domains',
            'main:contact',
            'main:faq',
            'main:industries',
            'main:favorites',
        ]

    def location(self, item):
        return reverse(item)
