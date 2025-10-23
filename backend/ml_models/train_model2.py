import sys, os
# Add the parent directory (backend/) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import Django and backendApp
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from backendApp.models import PlayerGameStat
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
from ml_models.data_preperation import add_recent_average_features

qs = PlayerGameStat.objects.all().values(
    'player_id',
    'game_date',
    'opponent',
    'home',
    'minutes',
    'points',
    'assists',
    'blocks',
    'steals',
    'fg_percent',
    'threepa',
    'threep',
    'threep_percent',
    'fta',
    'ft',
    'ft_percent',
    'total_rebounds',
    'personal_fouls',
    'turnovers'
)
df = pd.DataFrame(list(qs))

# Prepare data from data_preperation.py
df = add_recent_average_features(df)

# turn opponent into categorical codes
df['opponent'] = df['opponent'].fillna('Unknown')
df['opponent'] = df['opponent'].astype('category')
opponent_mapping = dict(enumerate(df['opponent'].cat.categories))
df['opponent'] = df['opponent'].cat.codes

X = df[['player_id', 'rest_days', 'opponent', 'home', 'avg_minutes_last5', 'avg_points_last5', 'avg_assists_last5', 'avg_blocks_last5', 'avg_steals_last5', 'avg_fg_percent_last5',
        'avg_threepa_last5', 'avg_threep_last5', 'avg_threep_percent_last5', 'avg_fta_last5', 'avg_ft_last5', 'avg_ft_percent_last5',
        'avg_total_rebounds_last5', 'avg_personal_fouls_last5', 'avg_turnovers_last5', 'avg_did_play_last10']]

y = df[['minutes', 'points', 'assists', 'blocks', 'steals', 'fg_percent',
        'threepa', 'threep', 'threep_percent', 'fta', 'ft', 'ft_percent',
        'total_rebounds', 'personal_fouls', 'turnovers']]

X_train, X_test, y_train, y_test = train_test_split(X ,y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_preds = model.predict(X_test)
print('R^2:', r2_score(y_test, y_preds, multioutput='uniform_average'))
print('MAE:', mean_absolute_error(y_test, y_preds))

joblib.dump(model, 'player_multioutput_projection.pkl')

print("model saved and trained successfully.")


