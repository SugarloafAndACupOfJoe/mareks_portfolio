from rest_framework import serializers
from .models import Pollutant


class PollutantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pollutant
        fields = '__all__'


