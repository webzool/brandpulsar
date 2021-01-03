import random
import uuid as uuid
import stripe
import syllables
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from treebeard.mp_tree import MP_Node
from main.managers import RecentBlogPostManager
from main.utils import get_file_path
from brandpulsar.utils import compress_image, disable_for_loaddata

User = get_user_model()


class Industry(MP_Node):
    name = models.CharField(
        _("Industry name"),
        max_length=100
    )
    featured = models.BooleanField(
        _("Featured"),
        default=False
    )
    icon = models.FileField(_("Icon"), null=True, blank=True, upload_to='industries/%Y/%m/%d/')
    slug = models.SlugField(
        _("Industry slug"),
        null=True,
        blank=True,
        default=None,
        max_length=50
    )
    content = RichTextUploadingField(
        null=True, blank=True
    )
    date_updated = models.DateTimeField(
        auto_now=True, null=True
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    node_order_by = ['name']

    objects = models.Manager()

    def featured_item(self):
        # Returns most expensive related domain item for object
        return self.industry.order_by('-price').first()

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)[:50]
            duplicate = Industry.objects.filter(slug=slug).first()
            if not duplicate:
                self.slug = slug
            else:
                self.slug = f"{slug}-{random.randint(1, 10)}"
        super(Industry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:industry-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name


class Tag(models.Model):
    title = models.CharField(_("Domain tag title"), max_length=250)

    def __str__(self):
        return self.title


class Plan(models.Model):
    domain = models.ForeignKey(
        "main.Domain",
        on_delete=models.CASCADE,
        related_name="plans",
        null=True)
    nickname = models.CharField(
        _("Plan Nickname"),
        max_length=50
    )
    unit_amount = models.DecimalField(
        _("Price per unit"),
        decimal_places=0,
        max_digits=20, null=True
    )
    plan_id = models.CharField(
        _("Plan ID"),
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.domain.name}.{self.domain.extension} - {self.nickname} month plan"


@disable_for_loaddata
def recurring_domain_create(sender, instance, *args, **kwargs):
    if not instance.plan_id:
        recurring = stripe.Price.create(
            unit_amount=int(instance.unit_amount * 100),
            nickname=instance.nickname,
            currency="usd",
            recurring={"interval": "month"},
            product=instance.domain.stripe_recurring_id,
        )

        instance.plan_id = recurring.id

    elif instance.plan_id:
        stripe.Price.modify(
            instance.plan_id,
            nickname=instance.nickname,
        )


pre_save.connect(recurring_domain_create, sender=Plan)


class Domain(models.Model):
    RATING = (
        ('bad', 'bad'),
        ('poor', 'poor'),
        ('fair', 'fair'),
        ('good', 'good'),
        ('excellent', 'excellent'),
    )
    STATUS = (
        ('available', 'AVAILABLE'),
        ('sold', 'SOLD')
    )
    ACTIVE_STATUS = (
        ('waiting', 'WAITING'),
        ('pending', 'PENDING'),
        ('listed', 'LISTED'),
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="domains"
    )
    name = models.CharField(_("Domain name"), max_length=200)
    length = models.PositiveIntegerField(
        _("Domain length"),
        blank=True, null=True
    )
    is_active = models.CharField(
        choices=ACTIVE_STATUS,
        default='waiting',
        max_length=10
    )
    extension = models.CharField(
        _("Domain extension"),
        max_length=150, null=True
    )
    stripe_recurring_id = models.CharField(
        _("Recurring product id"),
        max_length=150,
        null=True, blank=True
    )
    stripe_one_time_id = models.CharField(
        _("One time product id"),
        max_length=150,
        null=True, blank=True
    )
    price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    discount_price = models.DecimalField(
        _("Discount Price"),
        decimal_places=0,
        max_digits=20, null=True, blank=True
    )
    negotiable_price = models.DecimalField(
        _("Negotiable Domain price"),
        decimal_places=0,
        max_digits=20, null=True, blank=True
    )
    favorite_count = models.IntegerField(
        _("Favorite Count"),
        null=True,
        default=0,
        blank=True
    )
    featured = models.BooleanField(
        _("Featured"),
        default=False
    )
    domain_length = models.CharField(
        _("Domain length rating"),
        choices=RATING,
        blank=True,
        max_length=150
    )
    status = models.CharField(
        max_length=25,
        default='available',
        choices=STATUS,
        verbose_name=_("Status of the domain")
    )
    pronouncement = models.CharField(
        _("Domain pronouncement rating"),
        choices=RATING,
        default='available',
        blank=True,
        max_length=150
    )
    brandable = models.CharField(
        _("Domain brandable rating"),
        choices=RATING,
        blank=True, max_length=150
    )
    thumbnail_image = models.ImageField(
        _("Thumbnail image"),
        upload_to='domains/%Y/%m/%d/',
        null=True, blank=True
    )
    mockup_1 = models.FileField(
        _("Mockup 1"),
        upload_to='mockups/%Y/%m/%d/',
        null=True, blank=True
    )
    syllable = models.PositiveIntegerField(
        verbose_name=_("Syllable count"),
        null=True,
        blank=True
    )
    mockup_2 = models.FileField(
        _("Mockup 2"),
        upload_to='mockups/%Y/%m/%d/',
        null=True, blank=True
    )
    mockup_3 = models.FileField(
        _("Mockup 3"),
        upload_to='mockups/%Y/%m/%d/',
        null=True, blank=True
    )
    slug = models.SlugField(
        _("Domain slug"),
        null=True,
        unique=True,
        blank=True,
        default=None,
        max_length=250
    )
    date_updated = models.DateTimeField(auto_now=True, null=True)
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("Tags"),
        related_name="domains",
        blank=True
    )
    date_created = models.DateTimeField(
        _("Date Published"),
        default=timezone.now
    )
    industry = models.ManyToManyField(
        Industry,
        verbose_name=_("Industries"),
        related_name="industry",
        blank=True
    )
    visit_count = models.PositiveIntegerField(_("Visitor Count"), default=0)
    stripe_product_id = models.CharField(blank=True, null=True, max_length=120)
    featured_plan_id = models.CharField(blank=True, null=True, max_length=120)

    @property
    def ranking(self):
        return self.visit_count

    @property
    def get_related(self):
        tags = self.tags.all()
        industries = self.industry.all()
        queryset = Domain.objects.filter(
            tags__in=tags,
            industry__in=industries
        ).exclude(id=self.pk).distinct()
        return queryset

    def get_absolute_url(self):
        return reverse('main:domain-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.length = len(self.name)

        # Estimated syllable count from `syllables` package
        self.syllable = syllables.estimate(self.name)

        if self.thumbnail_image:
            self.thumbnail_image = compress_image(
                img=self.thumbnail_image,
                instance=self.__str__()
            )
        if self.mockup_1:
            self.mockup_1 = compress_image(
                img=self.mockup_1,
                instance=self.__str__()
            )
        if self.mockup_2:
            self.mockup_2 = compress_image(
                img=self.mockup_2,
                instance=self.__str__()
            )
        if self.mockup_3:
            self.mockup_3 = compress_image(
                img=self.mockup_3,
                instance=self.__str__()
            )
        if not self.owner:
            self.owner = User.objects.filter(is_superuser=True).first()
        if not self.slug:
            slug = slugify(f'{self.name}-{self.extension}')
            duplicate = Domain.objects.filter(slug=slug)
            if duplicate:
                slug = f"{slug}-1"
            self.slug = slug
        if not self.length:
            self.length = len(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}.{self.extension}'

    def get_absolute_url(self):
        return reverse('main:domain-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"


def update_stripe_details(instance, images, image, price):
    # TODO : Fix this function. It`s not appropriate solution and messy
    i = instance
    if not i.stripe_one_time_id and not i.stripe_recurring_id and not i.stripe_product_id:

        new_domain = stripe.Product.create(
            name=i.name,
            type="good",
            images=images,
            attributes=["name"]
        )
        sku = stripe.SKU.create(
            attributes={
                "name": i.name
            },
            price=int(price * 100),
            currency="usd",
            inventory={"type": "infinite"},
            product=new_domain.id
        )
        new_recurring_domain = stripe.Product.create(
            name=i.name,
            type="service",
            images=images
        )
        i.stripe_product_id = new_domain.id
        i.stripe_one_time_id = sku.id
        i.stripe_recurring_id = new_recurring_domain.id

    elif i.stripe_one_time_id and i.stripe_recurring_id and i.stripe_product_id:
        domain_update = stripe.Product.modify(
            i.stripe_product_id,
            name=i.name,
            images=images,
            attributes=["name"]
        )
        i.stripe_product_id = domain_update.id
        stripe.SKU.modify(
            i.stripe_one_time_id,
            image=image,
            attributes={
                "name": i.name
            },
            price=int(price * 100)
        )


@disable_for_loaddata
def domain_created_receiver(sender, instance, *args, **kwargs):
    # If domain has a discount price, it becomes
    # default price of the domain
    price = instance.price

    images = []
    image = None
    if instance.thumbnail_image:
        images = [f'https://brandpulsar.com/{instance.thumbnail_image.url}', ]
        image = images[0]

    if instance.discount_price:
        price = instance.discount_price

    if instance.is_active == "listed":
        update_stripe_details(
            instance=instance,
            images=images,
            image=image,
            price=price
        )

        if not instance.featured_plan_id:
            featured_plan = stripe.Price.create(
                unit_amount=1000,
                nickname="Featured",
                currency="usd",
                recurring={"interval": "month"},
                product=instance.stripe_product_id,
            )

            instance.featured_plan_id = featured_plan.id


pre_save.connect(domain_created_receiver, sender=Domain)


@disable_for_loaddata
def domain_update_receiver(sender, instance, *args, **kwargs):
    images = []
    image = None
    if instance.thumbnail_image:
        images = [f'https://brandpulsar.com/{instance.thumbnail_image.url}', ]
        image = images[0]

    if instance.is_active == "listed":
        update_stripe_details(
            instance=instance,
            images=images,
            image=image,
            price=instance.price
        )

        stripe.Product.modify(
            instance.stripe_product_id,
            images=images
        )
        stripe.SKU.modify(
            instance.stripe_one_time_id,
            image=image,
        )


post_save.connect(domain_update_receiver, sender=Domain)


def domain_plan_creator(sender, instance, created, *args, **kwargs):
    # Creates Plan (model) instances automatically

    # if domain has discount price, it becomes
    # default price for the domain
    price = instance.price
    if instance.discount_price:
        price = instance.discount_price

    if instance.is_active == 'listed' and instance.price:
        prices = {
            "3": int(float(price)) / 3,
            "6": int(float(price)) / 6,
        }
        Plan.objects.update_or_create(
            domain=instance, nickname='3',
            defaults={"unit_amount": prices.get("3")}
        )
        Plan.objects.update_or_create(
            domain=instance, nickname='6',
            defaults={"unit_amount": prices.get("6")}
        )


post_save.connect(domain_plan_creator, sender=Domain)


class BankWire(models.Model):
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    phone = models.CharField(_("Phone Number"), max_length=50)
    email = models.EmailField(_("Phone Number"), max_length=100)
    company = models.CharField(_("Company"), max_length=100, null=True)
    country = models.CharField(_("Country"), max_length=100, null=True)
    state = models.CharField(_("State / Province"), max_length=100, null=True)
    address = models.CharField(_("Address"), max_length=100, null=True)
    zip = models.CharField(_("Zip code"), max_length=100, null=True)

    class Meta:
        verbose_name = "Bank Wire Form"
        verbose_name_plural = "Contact Forms"

    def __str__(self):
        return self.email


class Contact(models.Model):
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    phone = models.CharField(_("Phone Number"), max_length=50)
    email = models.EmailField(_("Email"), max_length=100)
    message = models.TextField(_("Message"), max_length=100)

    class Meta:
        verbose_name = "Contact Form"
        verbose_name_plural = "Contact Forms"

    def __str__(self):
        return self.email


class Author(models.Model):
    uuid = models.UUIDField(
        _("Author uuid"), default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    position = models.CharField(
        _("Position"), max_length=80, null=True, default="", blank=True)
    picture = models.ImageField(
        _("Picture"), upload_to=get_file_path, null=True, blank=True)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class BlogCategory(models.Model):
    title = models.CharField(_("Category display title"), max_length=100)
    description = models.CharField(
        _("Category description"), max_length=150, null=True, blank=True, default=None)
    slug = models.SlugField(_("Category slug"), null=True,
                            blank=True, default=None, max_length=50)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        super(BlogCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:blog-category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.title


class BlogTag(models.Model):
    name = models.CharField(_("Tag name"), max_length=50)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(_("Blog post title"), max_length=250)
    metadescription = models.TextField(
        _("Meta description"), null=True, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    thumbnail_image = models.FileField(
        _("Thumbnail image"), upload_to='posts/%Y/%m/%d/')
    slug = models.SlugField(_("Post slug"), null=True,
                            blank=True, default=None, max_length=550)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    date_created = models.DateTimeField(
        _("Date Published"), default=timezone.now)
    author = models.ForeignKey(Author, verbose_name=_(
        "Authors"), related_name="posts", on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(
        BlogTag, verbose_name=_("Tags"), related_name="tags")
    objects = models.Manager()
    recent = RecentBlogPostManager()
    category = models.ForeignKey(
        BlogCategory,
        verbose_name=_("Blog category"),
        related_name="posts",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True)

    @property
    def authors_display_list(self):
        author_names = map(lambda author: author.full_name, self.authors.all())
        return ', '.join([str(x) for x in author_names])

    def get_related(self):
        tags = self.tags.all()

        blog_queryset = BlogPost.objects.filter(
            tags__in=tags).exclude(id=self.pk).distinct()

        blog_ids = list(map(lambda blog: blog.id, blog_queryset))

        blog_count = 3 if len(blog_ids) > 3 else len(blog_ids)

        random_blog_ids = random.sample(blog_ids, blog_count)

        queryset = BlogPost.objects.filter(id__in=random_blog_ids)

        return queryset

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:blog-post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


class Contacts(models.Model):
    domain = models.ForeignKey(
        Domain,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Domain"),
        related_name='contact_requests')
    email = models.EmailField(verbose_name=_('E-mail address'))
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    surname = models.CharField(verbose_name=_('Surname'), max_length=60)
    message = models.TextField(verbose_name=_('Message'))

    class Meta:
        verbose_name = _("Contact Request")
        verbose_name_plural = _("Contact Requests")

    def __str__(self):
        return f"{self.name} {self.surname}"


class Faq(models.Model):
    CATEGORIES = (
        ('buyer', _("Buyer")),
        ('seller', _("Seller")),
    )
    question = models.CharField(
        max_length=200
    )
    category = models.CharField(
        choices=CATEGORIES, max_length=100, default='buyer')
    content = RichTextUploadingField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _("Faq")
        verbose_name_plural = _("Faqs")

    def __str__(self):
        return f'{self.question}'


class Customer(models.Model):
    EMPLOYEES = (
        ('0-50', '0-50'),
        ('50-100', '50-100'),
        ('100-150', '100-150'),
        ('150-200', '150-200'),
        ('200-250', '200-250'),
    )
    name = models.CharField(_("Name"), max_length=250)
    location = models.CharField(_("Location"), max_length=250, null=True, blank=True)
    industry = models.CharField(_("Industry"), max_length=250, null=True, blank=True)
    employees = models.CharField(_("Employees"), choices=EMPLOYEES, blank=True, max_length=150)
    description = models.TextField(_("Description"), null=True, blank=True)
    quote = models.TextField(_("Quote"), null=True, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    thumbnail_image = models.FileField(_("Thumbnail image"), upload_to='customers/%Y/%m/%d/')
    slug = models.SlugField(_("Slug"), null=True, blank=True, default=None, max_length=550)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    date_created = models.DateTimeField(_("Date Published"), default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
