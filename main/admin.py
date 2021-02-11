from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from main.models import (
    Domain, Industry,
    BlogCategory, BlogPost, BlogTag,
    Author, Tag, Plan, Contacts,
    Faq, Customer
)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'discount_price', 'is_active']
    search_fields = ['name', 'tags__title']
    autocomplete_fields = ['tags', 'industry']
    list_editable = ['price', 'discount_price', 'is_active']
    readonly_fields = [
        'length',
        'slug',
        'syllable',
        'stripe_recurring_id',
        'stripe_one_time_id',
        'featured_plan_id'
    ]
    fieldsets = [
        ('Domain information',
         {'fields': [
             'owner',
             'name',
             'extension',
             'price',
             'favorite_count',
             'discount_price',
             'featured',
             'status',
             'is_active',
             'thumbnail_image']}
         ),
        ('Ratings',
         {'fields': [
             'domain_length',
             'pronouncement',
             'brandable']}
         ),
        ('Mockup images',
         {'fields': [
             'mockup_1',
             'mockup_2',
             'mockup_3']}
         ),
        ('Industries / Tags / Purpose',
         {'fields': [
             'tags',
             'industry']}
         ),
        ('Do not fill these fields',
         {'fields': [
             'date_created',
             'slug',
             'syllable',
             'length',
             'stripe_recurring_id',
             'stripe_one_time_id',
             'featured_plan_id',
             'stripe_product_id']}
         ),
    ]


@admin.register(Industry)
class IndustryAdmin(TreeAdmin):
    list_display = ['name', 'pk']
    search_fields = ['name']
    form = movenodeform_factory(Industry)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'email']


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question']


admin.site.register(Plan)

admin.site.register(BlogPost)

admin.site.register(BlogCategory)

admin.site.register(BlogTag)

admin.site.register(Author)

admin.site.register(Customer)
