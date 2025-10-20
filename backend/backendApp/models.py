from os import name
from django.db import models

class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=10)
    team = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SeasonStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='season_stats')
    season = models.CharField(max_length=10)
    team = models.CharField(max_length=10, null=True, blank=True)

    games_played = models.IntegerField(null=True, blank=True)
    minutes = models.FloatField(null=True, blank=True)
    fg_percent = models.FloatField(null=True, blank=True)
    threep_percent = models.FloatField(null=True, blank=True)
    ft_percent = models.FloatField(null=True, blank=True)
    rebounds = models.FloatField(null=True, blank=True)
    assists = models.FloatField(null=True, blank=True)
    steals = models.FloatField(null=True, blank=True)
    blocks = models.FloatField(null=True, blank=True)
    turnovers = models.FloatField(null=True, blank=True)
    personal_fouls = models.FloatField(null=True, blank=True)
    points = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('player', 'season', 'team')
        ordering = ['player', 'season']

class PlayerGameStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_game_stats')
    game_date = models.CharField(max_length=20, null=True, blank=True)
    game_type = models.CharField(max_length=100, null=True, blank=True)
    team = models.CharField(max_length=100, null=True, blank=True)
    opponent = models.CharField(max_length=100, null=True, blank=True)
    win = models.IntegerField(null=True, blank=True)
    home = models.IntegerField(null=True, blank=True)
    minutes = models.FloatField(null=True, blank=True)
    points = models.FloatField(null=True, blank=True)
    assists = models.FloatField(null=True, blank=True)
    blocks = models.FloatField(null=True, blank=True)
    steals = models.FloatField(null=True, blank=True)
    fg_percent = models.FloatField(null=True, blank=True)
    threepa = models.FloatField(null=True, blank=True)
    threep = models.FloatField(null=True, blank=True)
    threep_percent = models.FloatField(null=True, blank=True)
    fta = models.FloatField(null=True, blank=True)
    ft = models.FloatField(null=True, blank=True)
    ft_percent = models.FloatField(null=True, blank=True)
    total_rebounds = models.FloatField(null=True, blank=True)
    personal_fouls = models.FloatField(null=True, blank=True)
    turnovers = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['game_date']


