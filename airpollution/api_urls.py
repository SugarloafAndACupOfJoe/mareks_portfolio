from django.urls import include, path
from rest_framework import routers

from .apis import CountryViewSet, PollutantViewSet


router = routers.DefaultRouter()
router.register('pollutant', PollutantViewSet)
router.register('country', CountryViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
