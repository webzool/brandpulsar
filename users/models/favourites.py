from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Favourites(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="favourites",
        verbose_name = "Customer"
    )
    domains = models.ManyToManyField(
        "main.Domain",
        related_name='favourites',
        verbose_name = "Domain list",
        blank=True
    )

    class Meta:
        verbose_name = "Favourite"
        verbose_name_plural = "Favourites"
    
    def __str__(self):
        return f'{self.user} - favourites'