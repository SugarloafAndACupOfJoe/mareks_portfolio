from rest_framework import serializers
from .models import Country, Pollutant


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('iso_code', 'name', 'color', 'removed', 'longitude', 'latitude', 'altitude')


class PollutantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pollutant
        fields = '__all__'


