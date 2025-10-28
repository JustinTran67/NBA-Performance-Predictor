# for feature engineering of rolling averages, etc.
import pandas as pd
import numpy as np

def add_recent_average_features(df):
    #turn 'game_date' into actual datetime
    df['game_date'] = pd.to_datetime(df['game_date'], errors='coerce')

    df = df.sort_values(['player_id', 'game_date'], ascending=[True, True]).copy() # Added ascending=True to ensure proper calculation of rolling averages.

    # check for null minutes and list it as 'did_play' = 0
    df['did_play'] = df['minutes'].apply(lambda x: 1 if x and x > 0 else 0)

    df['rest_days'] = (
        df.groupby('player_id')['game_date']
        .diff()
        .dt.days
        .fillna(0)
    )
    # cap rest days at 10
    df['rest_days'] = df['rest_days'].clip(upper=10)

    stat_fields = [
        'minutes', 'points', 'assists', 'blocks', 'steals', 'fg_percent',
        'threepa', 'threep', 'threep_percent', 'fta', 'ft', 'ft_percent',
        'total_rebounds', 'personal_fouls', 'turnovers'
    ]

    df[stat_fields] = df[stat_fields].fillna(0)

    valid_games = df[df['did_play'] == 1]

    # rolling fields: last_5, etc.
    for field in stat_fields:
        df[f'avg_{field}_last5'] = (
            valid_games.groupby('player_id')[field]
              .rolling(window=5, min_periods=1)
              .mean()
              .reset_index(level=0, drop=True)
        )
        df[f'avg_{field}_last5'] = df.groupby('player_id')[f'avg_{field}_last5'].transform(
            lambda x: x.fillna(x.mean())
        )

    # feature engineer participation rate
    df['avg_did_play_last10'] = (
        df.groupby('player_id')['did_play']
        .rolling(window=10, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    return df
