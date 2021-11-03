from rest_framework import viewsets

from .models import Pollutant
from .serializers import PollutantSerializer


class PollutantViewSet(viewsets.ModelViewSet):
    queryset = Pollutant.objects.all()
    serializer_class = PollutantSerializer
