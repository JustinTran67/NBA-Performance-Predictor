import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from backendApp.models import Player

class Command(BaseCommand):
    help = 'Import player team from CSV files'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        latest_entries = {}

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                player_name = row['firstName'].strip() + ' ' + row['lastName'].strip()
                team = row['playerteamCity'] + ' ' + row['playerteamName']
                date = row.get('gameDate')

                try:
                    date = datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    continue

                if player_name not in latest_entries or date > latest_entries[player_name]['date']:
                    latest_entries[player_name] = {'team': team, 'date': date}

        for player_name, data in latest_entries.items():
            Player.objects.update_or_create(
                    name = player_name,
                    defaults = {
                        'team' : data['team'],
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported current player teams'))