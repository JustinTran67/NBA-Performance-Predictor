from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, SeasonStatViewSet, PredictionViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'stats', SeasonStatViewSet)
router.register(r'predictions', PredictionViewSet, basename='predictions')

urlpatterns = [
    path('', include(router.urls)),

    #JWT authentication endpoints for obtaining and refreshing tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]