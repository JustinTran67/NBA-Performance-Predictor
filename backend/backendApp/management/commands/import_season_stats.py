import csv
from django.core.management.base import BaseCommand
from backendApp.models import Player, SeasonStat

def parse_float(value):
        if value in ('', 'NA', 'N/A'):
            return None
        try:
            return float(value)
        except ValueError:
            return None

class Command(BaseCommand):
    help = 'Import season stats from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')
    
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                player_name = row['player'].strip()
                season = row['season'].strip()

                #Create or get the player first
                player, _ = Player.objects.get_or_create(name=player_name)

                #Then create the season stat
                SeasonStat.objects.update_or_create(
                    player = player,
                    season = season,
                    team = row['team'],

                    defaults = {
                        'games_played' : int(row['g']),
                        'minutes' : parse_float(row['mp_per_game']),
                        'fg_percent' : parse_float(row['fg_percent']),
                        'threep_percent' : parse_float(row['x3p_percent']),
                        'ft_percent' : parse_float(row['ft_percent']),
                        'rebounds' : parse_float(row['trb_per_game']),
                        'assists' : parse_float(row['ast_per_game']),
                        'steals' : parse_float(row['stl_per_game']),
                        'blocks' : parse_float(row['blk_per_game']),
                        'turnovers' : parse_float(row['tov_per_game']),
                        'personal_fouls' : parse_float(row['pf_per_game']),
                        'points' : parse_float(row['pts_per_game']),
                    }
                )
            
        self.stdout.write(self.style.SUCCESS('Successfully imported season stats'))


