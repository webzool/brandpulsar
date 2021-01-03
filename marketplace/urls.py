from django.urls import path
from . import views

app_name='marketplace'

urlpatterns = [
    path('become-a-seller/', views.BecomeASellerView.as_view(), name='become-a-seller'),
    path('create/', views.DomainCreateView.as_view(), name='create-domain'),
    path('setup/<int:pk>/', views.DomainSetupView.as_view(), name='setup-domain'),
    path('update/<int:pk>/', views.DomainUpdateView.as_view(), name='update-domain'),
    path('delete/<int:pk>/', views.DomainDeleteView.as_view(), name='delete-domain'),
    path('brainstorming/', views.BrainStormingView.as_view(), name="brainstorming-view"),
]