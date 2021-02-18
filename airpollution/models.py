from django.db import models


class Pollutant(models.Model):
    """Pollution model for airpollution app"""
    name = models.CharField(max_length=10, primary_key=True)
    limit_value = models.SmallIntegerField(null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'pollutants'


class Country(models.Model):
    """Country model for airpollution app"""
    iso_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    removed = models.BooleanField(default=False)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    altitude = models.FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'countries'


class PollutantEntry(models.Model):
    """PolutantEntry model for airpollution app"""
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, related_name='entries')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='entries')
    year = models.IntegerField()
    city = models.CharField(max_length=50, default='', blank=True)
    station_code = models.CharField(max_length=20, default='', blank=True)
    station_name = models.CharField(max_length=100, default='', blank=True)
    pollution_level = models.FloatField()
    units = models.CharField(max_length=10, default='', blank=True)
    station_type = models.CharField(max_length=20, default='', blank=True)
    station_area = models.CharField(max_length=20, default='', blank=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    altitude = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} {self.pollutant.name} {self.year}'

    class Meta:
        verbose_name_plural = 'pollutant entries'
