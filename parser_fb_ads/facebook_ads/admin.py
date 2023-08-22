from django.contrib import admin

from facebook_ads.models import *


@admin.register(Keywords)
class Keywords_Admin(admin.ModelAdmin):
    list_display = ('query', )

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('status', 'date', 'platforms', 'audience_size', 'payment', 'impressions', 'name_author', 'link',)

@admin.register(CountrySettings)
class CountrySettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'active')
    search_fields = ('name', )
    list_editable = ('active', )

@admin.register(AdTypeSettings)
class AdTypeSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_editable = ('active', )
