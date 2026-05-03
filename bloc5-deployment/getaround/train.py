"""
Script de réentraînement local du modèle GetAround Pricing.
Génère getaround_model.pkl compatible avec la version sklearn locale.
"""
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "get_around_pricing_project.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "getaround_model.pkl")

# Chargement
print("📂 Chargement des données...")
df = pd.read_csv(DATA_PATH)
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

# Features
TARGET = "rental_price_per_day"
cat_cols = ["model_key", "fuel", "paint_color", "car_type"]
bool_cols = ["private_parking_available", "has_gps", "has_air_conditioning",
             "automatic_car", "has_getaround_connect", "has_speed_regulator", "winter_tires"]
num_cols = ["mileage", "engine_power"]

y = df[TARGET]
X = df.drop(columns=[TARGET])
X[bool_cols] = X[bool_cols].astype(int)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline
preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), num_cols + bool_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", GradientBoostingRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.1, random_state=42
    ))
])

# Entraînement
print("🤖 Entraînement du modèle...")
pipeline.fit(X_train, y_train)

# Évaluation
y_pred = pipeline.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print(f"✅ RMSE: {rmse:.2f} | R²: {r2:.3f}")

# Export
joblib.dump(pipeline, MODEL_PATH)
print(f"💾 Modèle sauvegardé : {MODEL_PATH}")

# Test rapide
sample = pd.DataFrame([{
    "model_key": "Renault", "mileage": 50000, "engine_power": 120,
    "fuel": "diesel", "paint_color": "grey", "car_type": "sedan",
    "private_parking_available": 1, "has_gps": 1, "has_air_conditioning": 1,
    "automatic_car": 0, "has_getaround_connect": 1, "has_speed_regulator": 0,
    "winter_tires": 0
}])
pred = pipeline.predict(sample)[0]
print(f"🔮 Test prédiction (Renault diesel 120ch) : {pred:.1f} €/jour")