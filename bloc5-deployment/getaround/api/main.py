import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

# Chargement du modele (meme dossier sur HuggingFace)
model = joblib.load("getaround_model.pkl")

app = FastAPI(
    title="GetAround Pricing API",
    description="API de prediction du prix journalier de location de voitures",
    version="1.0"
)


class PredictInput(BaseModel):
    model_key: str
    mileage: int
    engine_power: int
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: int
    has_gps: int
    has_air_conditioning: int
    automatic_car: int
    has_getaround_connect: int
    has_speed_regulator: int
    winter_tires: int

class PredictInputList(BaseModel):
    input: List[PredictInput]


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GetAround Pricing API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8f9fa; color: #333; min-height: 100vh; }
            header { background: linear-gradient(135deg, #e63946, #c1121f); color: white; padding: 40px; text-align: center; }
            header h1 { font-size: 2.2em; margin-bottom: 8px; }
            header p { font-size: 1.1em; opacity: 0.9; }
            .badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 0.85em; margin-top: 10px; }
            .container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
            .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; margin-bottom: 40px; }
            .card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); border-left: 4px solid #e63946; text-decoration: none; color: inherit; transition: transform 0.2s; }
            .card:hover { transform: translateY(-3px); }
            .card .icon { font-size: 2em; margin-bottom: 10px; }
            .card h3 { font-size: 1.1em; margin-bottom: 6px; color: #e63946; }
            .card p { font-size: 0.9em; color: #666; line-height: 1.5; }
            .section { background: white; border-radius: 12px; padding: 28px; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
            .section h2 { font-size: 1.3em; margin-bottom: 16px; color: #333; border-bottom: 2px solid #f1f3f5; padding-bottom: 10px; }
            .endpoint { display: flex; align-items: flex-start; gap: 14px; margin-bottom: 18px; padding-bottom: 18px; border-bottom: 1px solid #f1f3f5; }
            .endpoint:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
            .method { display: inline-block; padding: 4px 12px; border-radius: 6px; font-weight: bold; font-size: 0.8em; color: white; min-width: 60px; text-align: center; flex-shrink: 0; margin-top: 2px; }
            .get { background: #2a9d8f; }
            .post { background: #e76f51; }
            .endpoint-info h4 { font-size: 1em; margin-bottom: 4px; }
            .endpoint-info p { font-size: 0.88em; color: #666; }
            code { background: #f1f3f5; padding: 2px 7px; border-radius: 4px; font-size: 0.88em; font-family: 'Courier New', monospace; }
            .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
            .stat { background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
            .stat .value { font-size: 1.8em; font-weight: bold; color: #e63946; }
            .stat .label { font-size: 0.85em; color: #666; margin-top: 4px; }
            pre { background: #2d2d2d; color: #f8f8f2; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 0.82em; line-height: 1.5; margin-top: 10px; }
            footer { text-align: center; padding: 30px; color: #999; font-size: 0.85em; }
        </style>
    </head>
    <body>
        <header>
            <div style="font-size:3em; margin-bottom:12px;">🚗</div>
            <h1>GetAround Pricing API</h1>
            <p>Prediction du prix journalier optimal pour la location de voitures</p>
            <div class="badge">GradientBoostingRegressor - R2=0.756 - RMSE=16EUR - v1.0</div>
        </header>
        <div class="container">
            <div class="stats">
                <div class="stat"><div class="value">0.756</div><div class="label">R2 score (test)</div></div>
                <div class="stat"><div class="value">16EUR</div><div class="label">RMSE moyen</div></div>
                <div class="stat"><div class="value">4 843</div><div class="label">Voitures entrainées</div></div>
            </div>
            <div class="cards">
                <a href="/docs" class="card"><div class="icon">📄</div><h3>Documentation interactive</h3><p>Swagger UI - testez les endpoints directement dans votre navigateur</p></a>
                <a href="/health" class="card"><div class="icon">💚</div><h3>Health Check</h3><p>Verifiez le statut de l'API et les informations du modele deploye</p></a>
                <a href="/redoc" class="card"><div class="icon">📋</div><h3>ReDoc</h3><p>Documentation alternative au format ReDoc</p></a>
            </div>
            <div class="section">
                <h2>Endpoints disponibles</h2>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <div class="endpoint-info"><h4><code>/health</code></h4><p>Verifie que l'API est operationnelle.</p></div>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <div class="endpoint-info"><h4><code>/predict</code></h4><p>Predit le prix journalier optimal. Accepte un JSON avec une cle <code>input</code>.</p></div>
                </div>
            </div>
            <div class="section">
                <h2>Exemple curl</h2>
                <pre>curl -X POST "https://your-url/predict" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"model_key": "Renault", "mileage": 50000, "engine_power": 120,
  "fuel": "diesel", "paint_color": "grey", "car_type": "sedan",
  "private_parking_available": 1, "has_gps": 1, "has_air_conditioning": 1,
  "automatic_car": 0, "has_getaround_connect": 1, "has_speed_regulator": 0,
  "winter_tires": 0}]}'</pre>
                <p style="margin-top:12px; font-size:0.9em; color:#666;">Reponse attendue :</p>
                <pre>{"prediction": [147.9]}</pre>
            </div>
        </div>
        <footer>GetAround Pricing API - Jedha CDSD Bloc 5 - Deploiement 2026</footer>
    </body>
    </html>
    """


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": "GradientBoostingRegressor",
        "r2_score": 0.756,
        "rmse": 16.02,
        "version": "1.0"
    }


@app.post("/predict")
def predict(data: PredictInputList):
    df = pd.DataFrame([item.dict() for item in data.input])
    predictions = model.predict(df)
    return {"prediction": [round(float(p), 2) for p in predictions]}
