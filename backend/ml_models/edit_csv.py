# purpose: adjust the file of PlayerStatistics.csv to only include data from 2000 and later.

from email.utils import format_datetime
import os
import pandas as pd

path = os.path.join('ml_models', 'PlayerStatistics.csv')
df = pd.read_csv(path)

df['gameDate'] = pd.to_datetime(df['gameDate'].astype(str).str[:10], errors='coerce').dt.date

df_recent = df[df['gameDate'] >= pd.to_datetime('2022-01-01').date()].copy()

df_recent.loc[df_recent['playerteamCity'] == 'LA', 'playerteamCity'] = 'Los Angeles'

df_recent.loc[df_recent['opponentteamCity'] == 'LA', 'opponentteamCity'] = 'Los Angeles'

df_recent.to_csv("PlayerStatistics_Recent.csv", index = False)

print(f'reduced from {len(df)} to {len(df_recent)} rows')