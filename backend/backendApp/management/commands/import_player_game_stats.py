import csv
from django.core.management.base import BaseCommand
from backendApp.models import Player, PlayerGameStat

def parse_float(value):
    if value in ('', 'NA', 'N/A'):
        return None
    try:
        return float(value)
    except ValueError:
        return None
    
class Command(BaseCommand):
    help = "Import player game stats from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')
    
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                player_name = row['firstName'].strip() + ' ' + row['lastName'].strip()

                player, _ = Player.objects.get_or_create(name=player_name)

                PlayerGameStat.objects.create(
                    player = player,
                    game_date = row['gameDate'],
                    game_type = row['gameType'],
                    team = row['playerteamCity'] + ' ' + row['playerteamName'],
                    opponent = row['opponentteamCity'] + ' ' + row['opponentteamName'],
                    win = int(row['win']) if row['win'] else None,
                    home = int(row['home']) if row['home'] else None,
                    minutes = parse_float(row['numMinutes']),
                    points = parse_float(row['points']),
                    assists = parse_float(row['assists']),
                    blocks = parse_float(row['blocks']),
                    steals = parse_float(row['steals']),
                    fg_percent = parse_float(row['fieldGoalsPercentage']),
                    threepa = parse_float(row['threePointersAttempted']),
                    threep = parse_float(row['threePointersMade']),
                    threep_percent = parse_float(row['threePointersPercentage']),
                    fta = parse_float(row['freeThrowsAttempted']),
                    ft = parse_float(row['freeThrowsMade']),
                    ft_percent = parse_float(row['freeThrowsPercentage']),
                    total_rebounds = parse_float(row['reboundsTotal']),
                    personal_fouls = parse_float(row['foulsPersonal']),
                    turnovers = parse_float(row['turnovers']),
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported player game stats'))
        
