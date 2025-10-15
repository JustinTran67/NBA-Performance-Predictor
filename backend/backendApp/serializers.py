from rest_framework import serializers
from .models import Player, SeasonStat, Prediction

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class SeasonStatSerializer(serializers.ModelSerializer):
    #Optional player information stored inside seasonstat.
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = SeasonStat
        fields = '__all__'

