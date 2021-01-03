from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "users"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register-view"),
    path('activate/', views.ActivateView.as_view(), name="register-done-view"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('activate/<uidb64>/<token>/',
         views.ActivateView.as_view(),
         name="activate-view"),
    path('login/', views.LoginView.as_view(), name="login-view"),
    path('logout/', views.LogOutView.as_view(), name="logout-view"),
    path(
        'password/reset/',
        views.CustomPasswordResetView.as_view(),
        name="password-reset"),
    path(
        'password/confirm/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm"),
    path(
        'password/done/',
        views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_complete"),
    path('edit/',
         login_required(views.UserEditView.as_view()),
         name="user-edit-view"),
    path('edit/password/',
         login_required(views.UserPasswordEditView.as_view()),
         name="user-edit-password-view"),
    # path(
    #     'payment-methods/',
    #     views.PaymentMethodListView.as_view(),
    #     name="payment-method-list"
    # ),
    # path(
    #    'add/payment-method/',
    #    views.PaymentMethodCreateView.as_view(),
    #    name="add-payment-method"
    # ),
    # path(
    #    'update/payment-method/<int:pk>/',
    #    views.PaymentMethodUpdateView.as_view(),
    #    name="update-payment-method"
    # ),
    # path(
    #    'delete/payment-method/<int:pk>/',
    #    views.PaymentMethodDeleteView.as_view(),
    #    name="delete-payment-method",
    # ),
    # path('payment-history/', views.PaymentHistoryView.as_view(),
    #      name="payment-history",)
]
