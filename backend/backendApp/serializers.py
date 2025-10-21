from rest_framework import serializers
from .models import Player, SeasonStat, PlayerGameStat

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class SeasonStatSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = SeasonStat
        fields = '__all__'

class PlayerGameStatSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = PlayerGameStat
        fields = '__all__'
