from rest_framework import viewsets
from .models import Player, SeasonStat
from .serializers import PlayerSerializer, SeasonStatSerializer
#Check if this is still needed and find the difference between these two imports and viewsets.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_api(request):
    data = {
        'message': 'Hello from Django!'
    }
    return Response(data) 

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class SeasonStatViewSet(viewsets.ModelViewSet):
    queryset = SeasonStat.objects.all()
    serializer_class = SeasonStatSerializer

    #season filter
    def get_queryset(self):
        season = self.request.query_params.get('season')
        if season:
            return SeasonStat.objects.filter(season=season)
        return SeasonStat.objects.all()

