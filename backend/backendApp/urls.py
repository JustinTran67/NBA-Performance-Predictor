from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, SeasonStatViewSet

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'stats', SeasonStatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]