from django.contrib import admin
from .models import Player, SeasonStat, Prediction

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'team', 'height', 'weight')
    
@admin.register(SeasonStat)
class SeasonStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'season', 'team', 'games_played', 'points', 'rebounds', 'assists', 'blocks', 'steals')
    list_filter = ('season', 'team')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('player', 'season', 'predicted_points', 'predicted_rebounds', 'predicted_assists', 'created_at')
    list_filter = ('season',)


