import random

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify
from brandpulsar.utils import compress_image


class UserManager(UserManager):
    """
    Manager for custom user model.
    """

    def create_user(self, email, password=None):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user

    def _format_date_param(self, date):
        return date.replace("/", "-")


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as main auth field.
    """
    GROUP_NAMES = ["New customer", "Elite user", "Standard user"]
    USER_TYPE = (
        (1, 'Buyer'), (2, 'Seller')
    )
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True,)
    name = models.CharField(
        max_length=80,
        verbose_name="Name",
        blank=True, null=True
    )
    surname = models.CharField(
        max_length=80,
        verbose_name="Surname",
        blank=True, null=True
    )
    stripe_id = models.CharField(
        max_length=80,
        verbose_name="Stripe ID",
        blank=True, null=True
    )
    profile_picture = models.ImageField(
        upload_to="pp",
        verbose_name = "Profile Picture",
        null=True, blank=True
    )
    phone = models.CharField(
        max_length=80,
        verbose_name="Phone Number",
        blank=True, null=True
    )
    user_type = models.PositiveIntegerField(
        default=1,
        choices=USER_TYPE,
        verbose_name="User Type"
    )
    slug = models.SlugField(
        max_length=255, unique=True, 
        blank=True, editable=False
    )
    is_active = models.BooleanField(verbose_name="Active", default=False)
    is_staff = models.BooleanField(verbose_name="Staff", default=False)

    # Additional information
    current_sign_in_ip = models.GenericIPAddressField(
        blank=True, null=True, 
        verbose_name="Current IP"
    )
    last_signed_in_ip = models.GenericIPAddressField(
        blank=True, null=True, 
        verbose_name="Latest IP"
    )
    sign_in_count = models.IntegerField(
        default=0, verbose_name="Sign in count"
    )
    date_joined = models.DateTimeField(
        verbose_name="Joined on",
        auto_now_add=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.name} {self.surname}"
    
    @property
    def total_domain_values(self):
        return sum([domain.price for domain in self.domains.all()])
    
    @property
    def sold_domain_count(self):
        return len([domain for domain in self.domains.all() if domain.status == 'sold'])
    
    @property
    def total_earned(self):
        return sum([domain.price for domain in self.domains.all() if domain.status == 'sold'])
    
    def generate_slug(self):
        slug = slugify(self.__str__())
        unique_slug = slug
        extension = 1
        while User._default_manager.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{extension}"
            extension += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        if self.profile_picture:
            self.profile_picture = compress_image(
                img=self.profile_picture,
                instance=self.__str__()
            )
        return super().save(*args, **kwargs)