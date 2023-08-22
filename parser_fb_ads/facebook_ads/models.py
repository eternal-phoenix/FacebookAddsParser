from django.db import models


class Keywords(models.Model):
    query = models.CharField(max_length=255)

    def __str__(self):
        return self.query

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'


class Ad(models.Model):
    ad_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=250, null=True, blank=True)
    platforms = models.CharField(max_length=255, null=True, blank=True)
    audience_size = models.CharField(max_length=255, null=True, blank=True)
    payment = models.CharField(max_length=255, null=True, blank=True)
    impressions = models.CharField(max_length=255, null=True, blank=True)
    name_author = models.CharField(max_length=250, null=True, blank=True)
    link = models.CharField(max_length=400, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_author

    class Meta:
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'


class CountrySettings(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Select Country'
        verbose_name_plural = 'Settings Countries'



class AdTypeSettings(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Select Ad Type'
        verbose_name_plural = 'Settings Ad Types'


