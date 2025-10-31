import csv
from django.core.management.base import BaseCommand
from backendApp.models import Player

class Command(BaseCommand):
    help = 'Import player positions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')
    
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        def is_true(value):
            return str(value).strip().lower() in ['true']

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                player_name = row['player']
                position = ''

                Player.objects.filter(name=player_name).update(position=position)

        self.stdout.write(self.style.SUCCESS('Successfully imported player positions'))