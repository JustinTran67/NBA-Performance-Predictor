from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Player, SeasonStat, PlayerGameStat
from .serializers import PlayerSerializer, SeasonStatSerializer, PlayerGameStatSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
import joblib
import numpy as np
import pandas as pd
import os
from django.conf import settings
from ml_models.data_preperation import add_recent_average_features

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
    
class PlayerGameStatViewSet(viewsets.ModelViewSet):
    queryset = PlayerGameStat.objects.all()
    serializer_class = PlayerGameStatSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['player__name', 'team', 'opponent', 'game_date']
    ordering_fields = ['points', 'rebounds', 'assists', 'steals', 'blocks']
    permission_classes = [IsAuthenticatedOrReadOnly]

class PredictionViewSet(viewsets.ModelViewSet):
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

class PlayerPredictionViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] #TODO: switch back to IsAuthenticatedOrReadOnly later
    model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'player_multioutput_projection.pkl')
    _model = None
    
    # lazy loading model to stop memory jam at runserver
    @classmethod
    def getModel(cls):
        if cls._model is None:
            cls._model = joblib.load(cls.model_path)
        return cls._model

    @action(detail=False, methods=['post'])
    def predict(self, request):
        try:
            player_name = request.data.get('player')
            opponent = request.data.get('opponent')
            home = request.data.get('home', 1)
            game_date_str = request.data.get('game_date', None)

            if not player_name or not opponent:
                return Response(
                    {'error' : 'Missing player or opponent field'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            player = Player.objects.filter(name__iexact=player_name).first()
            if not player:
                return Response(
                    {'error' : f'Player "{player_name}" not found.'},
                    status = status.HTTP_404_NOT_FOUND
                )
            
            qs = PlayerGameStat.objects.filter(player=player).order_by('-game_date')[:50].values( #filter in reverse game_date so you get newest games!
                'player_id',
                'game_date',
                'opponent',
                'home',
                'minutes',
                'points',
                'assists',
                'blocks',
                'steals',
                'fg_percent',
                'threepa',
                'threep',
                'threep_percent',
                'fta',
                'ft',
                'ft_percent',
                'total_rebounds',
                'personal_fouls',
                'turnovers'
            )

            df = pd.DataFrame(list(qs))
            if df.empty:
                return Response(
                    {'error' : f'No game stats found for player "{player_name}".'},
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            df['game_date'] = pd.to_datetime(df['game_date'])
            last_game_date = df['game_date'].max()

            if game_date_str:
                game_date = pd.to_datetime(game_date_str)
            else: 
                game_date = last_game_date + pd.Timedelta(days=1)

            # append future game row for rest days calculation.
            df = pd.concat([df, pd.DataFrame([{
                'player_id': player.pk,
                'game_date': game_date,
                'opponent': opponent,
                'home': home,
                'minutes': None,
                'points': None,
                'assists': None,
                'blocks': None,
                'steals': None,
                'fg_percent': None,
                'threepa': None,
                'threep': None,
                'threep_percent': None,
                'fta': None,
                'ft': None,
                'ft_percent': None,
                'total_rebounds': None,
                'personal_fouls': None,
                'turnovers': None,
            }])])
            
            df = add_recent_average_features(df)

            df['opponent'] = df['opponent'].astype('category').cat.codes

            #get latest stats
            latest = df.sort_values('game_date').iloc[-1]

            feature_cols = [
                'player_id',
                'rest_days',
                'opponent',
                'home',
                'avg_minutes_last5',
                'avg_points_last5',
                'avg_assists_last5',
                'avg_blocks_last5',
                'avg_steals_last5',
                'avg_fg_percent_last5',
                'avg_threepa_last5',
                'avg_threep_last5',
                'avg_threep_percent_last5',
                'avg_fta_last5',
                'avg_ft_last5',
                'avg_ft_percent_last5',
                'avg_total_rebounds_last5',
                'avg_personal_fouls_last5',
                'avg_turnovers_last5',
                'avg_did_play_last10'
            ]
            features = latest[feature_cols].values.reshape(1, -1)

            model = self.getModel()
            prediction = model.predict(features)[0] #I do this because the model is multi-output

            stat_names = [
                'minutes', 'points', 'assists', 'blocks', 'steals', 'fg_percent',
                'threepa', 'threep', 'threep_percent', 'fta', 'ft', 'ft_percent',
                'total_rebounds', 'personal_fouls', 'turnovers'
            ]
            result = dict(zip(stat_names, prediction))
            return Response({
                'player': player_name,
                'opponent': opponent,
                'predictions': result,
            })
        
        except Exception as e:
            return Response(
                {'error' : str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )