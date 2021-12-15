from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Country, Pollutant
from .serializers import CountrySerializer, PollutantSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    # C
    # def create(self, request, *args, **kwargs):
    #     # Example
    #     if not (request.user.is_authenticated or request.data.get("auth_token") == "some_super_secret_token"):
    #         return Response({"error": "not authorised"}, status=status.HTTP_401_UNAUTHORIZED)
    #     return super().create(request, *args, **kwargs)
    #
    # # R
    # def retrieve(self, request, *args, **kwargs):
    #     # Example
    #     result = super().retrieve(request, *args, **kwargs)
    #     if not request.user.is_authenticated:
    #         del result.data['longitude']
    #         del result.data['latitude']
    #         del result.data['altitude']
    #     return result
    #
    # # R
    # def list(self, request, *args, **kwargs):
    #     # Example
    #     result = super().list(request, *args, **kwargs)
    #     if not request.user.is_authenticated:
    #         del result.data[5:]
    #     return result
    #
    # # U
    # def update(self, request, *args, **kwargs):
    #     # Example
    #     # return super().update(request, *args, **kwargs)
    #     return Response({"error": "updates are not allowed via API"}, status=status.HTTP_400_BAD_REQUEST)
    #
    # # U
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)
    #
    # # D
    # def destroy(self, request, *args, **kwargs):
    #     # Example
    #     # return super().destroy(request, *args, **kwargs)
    #     return Response({"error": "deletions are not allowed via API"}, status=status.HTTP_400_BAD_REQUEST)


class PollutantViewSet(viewsets.ModelViewSet):
    queryset = Pollutant.objects.all()
    serializer_class = PollutantSerializer
