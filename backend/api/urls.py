from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet, search_schedule, LineViewSet

router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'lines', LineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', search_schedule, name='search_schedule'),
]
