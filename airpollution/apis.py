from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser

from .models import Country, Pollutant
from .serializers import CountrySerializer, PollutantSerializer


@csrf_exempt
def country(request):
    if request.method == 'GET':
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    if request.method == 'POST':
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = CountrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def country_detail(request, pk):
    try:
        country_instance = Country.objects.get(pk=pk)
    except Country.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CountrySerializer(country_instance)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    if request.method in ['PUT', 'PATCH']:
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = CountrySerializer(instance=country_instance, data=data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        country_instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


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
