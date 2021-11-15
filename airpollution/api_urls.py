from django.urls import include, path
from rest_framework import routers

from .apis import PollutantViewSet


router = routers.DefaultRouter()
router.register('', PollutantViewSet)


urlpatterns = [
    path('pollutant/', include(router.urls)),
]
