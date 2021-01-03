from django.urls import path
from . import views

urlpatterns = [
    path(
        'domains/',
        views.DomainListView.as_view(),
        name="domain-list-api"),
    path(
        'my-domains/',
        views.UsersDomainsListView.as_view(),
        name="my-domain-list-api"),
    path(
        'brainstorming/',
        views.DomainBrainStormingAPIView.as_view(),
        name="brainstorming-api"
    ),
    path(
        'domains/<int:pk>/',
        views.SingleDomainAPIView.as_view(),
        name="single-domain-api"),
    path(
        'autocomplete/',
        views.SearchAutoCompleteView.as_view(),
        name="autocomplete-api"),
    path(
        'favourite/',
        views.FavouriteAPIView.as_view(),
        name="favourite-api"),
    path(
        'contacts/',
        views.ContactsAPIView.as_view(),
        name="contact-api"),
    path(
        'negotiate/',
        views.NegotiateContactAPIView.as_view(),
        name="negotiate-api"),
    path(
        'appraisal/',
        views.DomainAppraisalAPIView.as_view(),
        name="domain-appraisal"),
    path(
        'verify/',
        views.VerifyDomainAPIView.as_view(),
        name="verify-domain-redirect"
    ),
]