from ast import Is
from rest_framework import viewsets, filters, status #what is status?
from rest_framework.response import Response #what is Response?
from rest_framework.decorators import action #what is action?
from .models import Player, SeasonStat, Prediction
from .serializers import PlayerSerializer, SeasonStatSerializer, PredictionSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
import joblib
import numpy as np #understand the role of this
import os #what is this?
from django.conf import settings #What is this?

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'team', 'position']
    permission_classes = [IsAuthenticatedOrReadOnly]

class SeasonStatViewSet(viewsets.ModelViewSet):
    queryset = SeasonStat.objects.all()
    serializer_class = SeasonStatSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['player__name', 'season', 'team']
    ordering_fields = ['points', 'rebounds', 'assists', 'steals', 'blocks']
    permission_classes = [IsAuthenticatedOrReadOnly]

    #season filter
    def get_queryset(self):
        season = self.request.query_params.get('season')
        if season:
            return SeasonStat.objects.filter(season=season)
        return SeasonStat.objects.all()

class PredictionViewSet(viewsets.ModelViewSet):
    #LEARN HOW ALL OF THIS WORKS! WHY NO SERIALIZER_CLASS?
    permission_classes = [AllowAny] #TODO: switch back to IsAuthenticatedOrReadOnly later
    model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'nba_predictor.pkl')
    model = joblib.load(model_path)

    @action(detail=False, methods=['post'])
    def predict(self, request):
        try:
            data = request.data
            features = [
                float(data.get('minutes', 0)),
                float(data.get('fg_percent', 0)),
                float(data.get('threep_percent', 0)),
                float(data.get('ft_percent', 0)),
                float(data.get('rebounds', 0)),
                float(data.get('assists', 0)),
                float(data.get('steals', 0)),
                float(data.get('blocks', 0)),
                float(data.get('turnovers', 0)),
                float(data.get('personal_fouls', 0)),
            ]
            prediction = self.model.predict([features])
            return Response({'predicted_points' : prediction[0]})
        
        except KeyError as e:
            return Response(
                {'error' : f'Missing field: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error' : str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

