import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error
import joblib

df = pd.read_csv('ml_models/Player_Per_Game.csv')

columns_needed = ['mp_per_game', 'fg_per_game', 'fga_per_game', 'fg_percent', 'x3pa_per_game', 'x3p_percent', 'ft_per_game', 'fta_per_game', 'ft_percent', 'orb_per_game', 'drb_per_game',  'tov_per_game', 'pf_per_game', 'pts_per_game', 'x3p_per_game', 'trb_per_game', 'ast_per_game', 'blk_per_game', 'stl_per_game']
df = df[columns_needed].dropna()

x = df[columns_needed[:-6]]
y = df['pts_per_game', 'x3p_per_game', 'trb_per_game', 'ast_per_game', 'blk_per_game', 'stl_per_game']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
model.fit(X_train, y_train)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
print(f"Mean Absolute Error: {mae:.2f}")

joblib.dump(model, 'ml_models/nba_predictor.pkl')