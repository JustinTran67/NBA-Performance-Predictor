#Integrated The bellow code because backendApp.models was not being read!
import sys, os
# Add the parent directory (backend/) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now Django and backendApp can be imported
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from backendApp.models import SeasonStat
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression #basic model
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib

qs = SeasonStat.objects.all().values()
df = pd.DataFrame(list(qs))

df = df.dropna(subset=['points', 'minutes', 'fg_percent', 'threep_percent', 'ft_percent', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'personal_fouls'])
X = df[['minutes', 'fg_percent', 'threep_percent', 'ft_percent', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'personal_fouls']]
y = df[['points']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("R^2:", r2_score(y_test, preds)) #closer to 1 is better
print("MSE:", mean_squared_error(y_test, preds)) #lower is better

joblib.dump(model, 'nba_predictor.pkl')