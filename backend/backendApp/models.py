from os import name
from django.db import models

class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=10)
    team = models.CharField(max_length=50)
    height = models.FloatField(null=True, blank=True, help_text="Height in inches")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in pounds")

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

#Might not need this model, but keeping for now.    
class Prediction(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='predictions')
    season = models.CharField(max_length=10)
    model_version = models.CharField(max_length=50, null=True, blank=True)

    predicted_points = models.FloatField(null=True, blank=True)
    predicted_threep = models.FloatField(null=True, blank=True)
    predicted_rebounds = models.FloatField(null=True, blank=True)
    predicted_assists = models.FloatField(null=True, blank=True)
    predicted_blocks = models.FloatField(null=True, blank=True)
    predicted_steals = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prediction for {self.player.name} ({self.season})"
