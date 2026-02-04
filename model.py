import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

BASE = os.path.dirname(__file__)
csv_path = os.path.join(BASE, "..", "dataset", "soil_data_500.csv")

data = pd.read_csv(csv_path)

X = data[['ph','moisture','n','p','k']]

y_soil = data['soil']
y_crop = data['crop']

soil_model = RandomForestClassifier(n_estimators=100)
crop_model = RandomForestClassifier(n_estimators=100)

soil_model.fit(X, y_soil)
crop_model.fit(X, y_crop)

joblib.dump(soil_model, "soil_model.pkl")
joblib.dump(crop_model, "crop_model.pkl")

print("✅ Both models trained and saved!")
