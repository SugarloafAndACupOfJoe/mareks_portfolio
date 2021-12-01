from rest_framework import viewsets

from .models import Country, Pollutant
from .serializers import CountrySerializer, PollutantSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    # C
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)

    # R
    def retrieve(self, request, *args, **kwargs):
        super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)

    # U
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    # U
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)

    # D
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)


class PollutantViewSet(viewsets.ModelViewSet):
    queryset = Pollutant.objects.all()
    serializer_class = PollutantSerializer
