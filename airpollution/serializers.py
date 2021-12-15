from rest_framework import serializers
from .models import Country, Pollutant


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('iso_code', 'name', 'color', 'removed', 'longitude', 'latitude', 'altitude')

    # C / U
    def save(self, **kwargs):
        return super().save(**kwargs)

    # C
    def create(self, validated_data):
        return super().create(validated_data)

    # U
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    # C / U
    def validate(self, attrs):
        # Only validates fields specified in serializer (above)
        return super().validate(attrs)

    # C / U
    def is_valid(self, raise_exception=False):
        return super().is_valid(raise_exception)

    # C / R / U
    @property
    def data(self):
        return super().data

    # C / U
    @property
    def validated_data(self):
        return super().validated_data


class PollutantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pollutant
        fields = '__all__'


