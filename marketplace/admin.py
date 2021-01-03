from django.contrib import admin

from marketplace.models import EstimatedDomainPrice, BrainstormingKeywords, DomainNegotiation

@admin.register(EstimatedDomainPrice)
class EstimatedDomainPriceAdmin(admin.ModelAdmin):
    list_display = ['domain', 'price']


@admin.register(BrainstormingKeywords)
class BrainStormingKeywordsAdmin(admin.ModelAdmin):
    list_display = ['key', 'count', 'get_industry', 'created_at']
    readonly_fields = ['industry', 'count', 'key']

    def get_industry(self, obj):
        return ", ".join(i.name for i in obj.industry.all())


@admin.register(DomainNegotiation)
class DomainNegotiationAdmin(admin.ModelAdmin):
    pass