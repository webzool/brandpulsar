from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

User = get_user_model()


class BasePayment(models.Model):
    email = models.EmailField()

    class Meta:
        abstract = True


class PayPalPayment(BasePayment):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="paypal_payment_methods"
    )
    class Meta:
        verbose_name = "PayPal Payment"
        verbose_name_plural = "PayPal Payment Methods"

    def __str__(self):
        return f"{self.user} - paypal payment method"


class CashAppPayment(BasePayment):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cashapp_payment_methods"
    )
    class Meta:
        verbose_name = "CashAPP Payment"
        verbose_name_plural = "CashAPP Payment Methods"

    def __str__(self):
        return f"{self.user} - paypal payment method"


class SkrillPayment(BasePayment):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skrill_payment_methods"
    )
    phone = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Skrill Payment"
        verbose_name_plural = "Skrill Payment Methods"

    def __str__(self):
        return f"{self.user} - paypal payment method"


class WirePayment(BasePayment):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wire_payment_methods"
    )
    account_number = models.CharField(max_length=200)
    routing_number = models.CharField(max_length=200)
    holder_first_name = models.CharField(max_length=200)
    holder_last_name = models.CharField(max_length=200)
    iban = models.CharField(max_length=200)
    swift = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Wire Payment"
        verbose_name_plural = "Wire Payment Methods"

    def __str__(self):
        return f"{self.user} - wire payment method"

class PaymentHistory(models.Model):
    types = (
        ('paypal', _('PayPal')),
        ('cashapp', _('CashAPP')),
        ('skrill', _('Skrill')),
        ('wire', _('Wire')),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    amount = models.DecimalField(
        _("Amount"),
        decimal_places=0, 
        max_digits=20, null=True
    )
    description = models.CharField(
        _("Description"),
        max_length=200,
        null=True, blank=True
    )
    method = models.CharField(choices=types, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Payment History")
        verbose_name_plural = _("Payment Histories")

    def __str__(self):
        return f'{self.user} - payment'