from django.contrib import admin
from .models import Player, SeasonStat, PlayerGameStat

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'team')
    
@admin.register(SeasonStat)
class SeasonStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'season', 'team', 'games_played', 'points', 'rebounds', 'assists', 'blocks', 'steals')
    list_filter = ('season', 'team')

@admin.register(PlayerGameStat)
class PlayerGameStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'game_date', 'game_type', 'team', 'opponent', 'win', 'home', 'minutes', 'points', 'assists', 'blocks', 'steals', 'fg_percent', 'threepa', 'threep', 'threep_percent', 'fta', 'ft', 'ft_percent', 'total_rebounds', 'personal_fouls', 'turnovers')
    list_filter = ('game_date',)


