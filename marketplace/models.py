from django.db import models
from django.utils.translation import ugettext as _


class EstimatedDomainPrice(models.Model):
    domain = models.CharField(max_length=50)
    price = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Estimated Domain Price"
        verbose_name_plural = "Estimated Domain Prices"

    def __str__(self):
        return f'{self.domain} - {self.price}'


class BrainstormingKeywords(models.Model):
    key = models.CharField(_("Main Key"), max_length=50)
    industry = models.ManyToManyField("main.Industry", blank=True)
    count = models.PositiveIntegerField(_("Count"), default=1)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = "Brainstorming Key"
        verbose_name_plural = "Brainstorming Keys"

    @property
    def industries(self):
        return ", ".join(item.name for item in self.industry.all())

    def __str__(self):
        return self.key


class DomainNegotiation(models.Model):
    domain = models.ForeignKey("main.Domain", on_delete=models.CASCADE )
    email = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    price = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Domain Negotiation"
        verbose_name_plural = "Domain Negotiations"

    def __str__(self):
        return f"{self.domain} deal from {self.email}"