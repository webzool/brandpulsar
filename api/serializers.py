from django.conf import settings
from rest_framework import serializers

from main.models import Domain, Industry, Tag, Contacts
from users.models import Favourites
from marketplace.models import DomainNegotiation


class TagReadSerialzier(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    class Meta:
        model = Tag
        fields = ['id', 'name', 'type']

    def get_name(self, obj):
        return obj.title
    
    def get_type(self, obj):
        return 'tag'


class IndustryReadSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Industry
        fields = ['id', 'name', 'url', 'type']
    
    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_type(self, obj):
        return 'industry'


class DomainReadSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = ['id', 'name', 'url', 'type']

    def get_url(self, obj):
        return obj.get_absolute_url()
    
    def get_type(self, obj):
        return 'domain'


class DomainSerializer(serializers.ModelSerializer):
    tags = TagReadSerialzier(many=True)
    industry = IndustryReadSerializer(many=True)
    full_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    ranking = serializers.SerializerMethodField()
    date_created = serializers.DateTimeField(format="%d.%m.%Y")
    date_updated = serializers.DateTimeField(format="%d.%m.%Y")

    class Meta:
        model = Domain
        exclude = ['stripe_recurring_id', 'stripe_one_time_id', 'stripe_product_id']
    
    def get_full_name(self, obj):
        return f'{obj.name}.{obj.extension}'
    
    def get_ranking(self, obj):
        return obj.ranking
    
    def get_url(self, obj):
        return obj.get_absolute_url()


class FavouritesSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(many=True)
    class Meta:
        model = Favourites
        fields = '__all__'


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"


class DomainNegotiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainNegotiation
        fields = '__all__'