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
