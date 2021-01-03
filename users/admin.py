from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import (
    Favourites,
    PayPalPayment,
    CashAppPayment,
    SkrillPayment,
    WirePayment,
    PaymentHistory
)

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'surname', 'date_joined']


@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):
    pass


@admin.register(PayPalPayment)
class PaypalAdmin(admin.ModelAdmin):
    pass


@admin.register(CashAppPayment)
class CashAppAdmin(admin.ModelAdmin):
    pass


@admin.register(SkrillPayment)
class SkrillAdmin(admin.ModelAdmin):
    pass


@admin.register(WirePayment)
class WireAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    pass
