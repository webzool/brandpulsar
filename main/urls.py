from django.urls import path, include
from main import views
from main.views import *
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import DomainSitemap, StaticViewSitemap

sitemaps = {
    'portfolio': DomainSitemap,
    'static': StaticViewSitemap
}

app_name = 'main'

urlpatterns = [
    # Static Pages
    path('', IndexView.as_view(), name='index'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('faq/', Faq.as_view(), name='faq'),
    path('how-it-works/', HowItWorks.as_view(), name='how-it-works'),
    path('knowledge-base/', KnowledgeBase.as_view(), name='knowledge-base'),
    path('terms-of-use/', TermsOfUse.as_view(), name='terms-of-use'),
    path('terms-of-service/', TermsOfService.as_view(), name='terms-of-service'),
    path('privacy-policy/', PrivacyPolicy.as_view(), name='privacy-policy'),
    # On Pages
    path('how-to-name-your-brand/', HowToNameYourBrand.as_view(), name='how-to-name-your-brand'),
    path('what-makes-a-name-brandable/', WhatMakesaNameBrandable.as_view(), name='what-makes-a-name-brandable'),
    # Helper Pages
    path('success/', Success.as_view(), name='success'),
    path('thank-you/', ThankYou.as_view(), name='thank-you'),
    path('cancel/', Canceled.as_view(), name='cancel'),
    path('create-session/', Session.as_view(), name='create-session'),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('create-customer-portal-session/', create_customer_portal_session, name='create-customer-portal-session'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('ajax-favorite', ajax_favorite_view, name='ajax_favorite_view'),
    path('mark-as-featured/', mark_as_featured, name='mark-as-featured'),
    # Business Names
    path('startup-names/', StartupNames.as_view(), name='startup-names'),
    path('website-names/', WebsiteNames.as_view(), name='website-names'),
    path('domain-names/', DomainNames.as_view(), name='domain-names'),
    path('company-names/', CompanyNames.as_view(), name='company-names'),
    # Blog
    path('blog/<slug:slug>/', SingleBlogPostView.as_view(), name='blog-post'),
    path('blog/categories/<slug:slug>/',
         SingleBlogCategoryView.as_view(), name='blog-category'),
    # Customers 
    path('customers/', Customers.as_view(), name='customers'),
    path('customers/<slug:slug>/', SingleCustomer.as_view(), name='single-customer'),
    # Domains
    path('domains/', DomainList.as_view(), name='domains'),
    path('domains/industries/<slug:slug>/',
         SingleIndustryView.as_view(), name='industry-detail'),
    path('domains/<slug:slug>/', SingleDomainView.as_view(), name='domain-detail'),
    path('industries/', IndustryListView.as_view(), name='industries'),
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', RobotsTXT.as_view(), name='robots.txt'),
    # Webhooks
    path('instalment-hooks/', instalment_webhook_view, name='instalment-hooks'),
    path('featured-hooks/', featured_webhook_view, name='featured-hooks'),
]

handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'
