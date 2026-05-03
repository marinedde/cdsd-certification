# 🚗 GetAround — Deployment Project

**Jedha CDSD — Bloc 5 : Industrialisation d'un algorithme d'apprentissage automatique**

---

## Context

[GetAround](https://www.getaround.com) is the Airbnb for cars. When renting a car, drivers book for a specific time period. It happens that drivers are late for checkout, which generates friction for the next driver if the car was supposed to be rented again on the same day.

This project addresses two objectives:
- **Data Analysis & Dashboard**: Help the Product Manager decide on a minimum delay threshold between two rentals
- **ML Pricing API**: Suggest optimum prices for car owners using Machine Learning

---

## Live Demo

| Service | URL |
|---------|-----|
| 📊 Dashboard Streamlit | https://huggingface.co/spaces/marinedde/getaround-dashboard |
| 🤖 FastAPI Pricing API | https://huggingface.co/spaces/marinedde/getaround-api |
| 📄 API Documentation | https://marinedde-getaround-api.hf.space/docs |

---

## Project Structure

```
getaround/
├── api/
│   ├── main.py                         # FastAPI app
│   └── Dockerfile                      # Docker configuration
├── streamlit_app/
│   └── streamlit_app.py                # Streamlit dashboard
├── models/
│   ├── train.py                        # Model training script
│   └── getaround_model.pkl             # Trained model (generated locally)
├── data/
│   └── .gitkeep                        # datasets not included (see Data section below)
├── notebooks/
│   └── 01-Getaround_analysis.ipynb     # EDA + ML notebook
└── requirements.txt
```

---

## Dashboard — Delay Analysis

Built with **Streamlit + Plotly**, the dashboard answers the Product Manager's key questions:

### Key findings

- **57.5%** of drivers return the car late (median delay: +9 min)
- **218 problematic cases** identified out of 1,841 chained rentals (11.8%)
- Mobile checkin generates more issues (61.4% late) than Connect (42.9%)

### Threshold recommendation

| Threshold | Cases solved | % solved | Rentals blocked | % revenue impact |
|-----------|-------------|----------|-----------------|------------------|
| 60 min | 102 / 218 | 46.8% | 401 | 1.9% |
| **120 min** | **147 / 218** | **67.4%** | **666** | **3.1%** |
| 180 min | 167 / 218 | 76.6% | 870 | 4.1% |
| 240 min | 177 / 218 | 81.2% | 1001 | 4.7% |

**Recommendation: 120 minutes — all cars** — best trade-off between solved cases and revenue impact.

### Dashboard pages

- **Vue generale** — KPIs, checkin type distribution, late return stats
- **Analyse des retards** — Delay distribution, time delta analysis
- **Simulateur de seuil** — Interactive threshold/scope simulator
- **Prediction de prix** — ML pricing prediction connected to the API

---

## ML Pricing API

### Model

- **Algorithm**: GradientBoostingRegressor
- **Features**: mileage, engine power, fuel, car type, paint color, 7 boolean equipment features
- **Target**: `rental_price_per_day`
- **Performance**: R²=0.756 | RMSE=16€ | trained on 4,843 cars

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage |
| GET | `/health` | API status |
| POST | `/predict` | Price prediction |
| GET | `/docs` | Interactive Swagger documentation |

### Usage

```bash
curl -X POST "https://marinedde-getaround-api.hf.space/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [{
      "model_key": "Renault",
      "mileage": 50000,
      "engine_power": 120,
      "fuel": "diesel",
      "paint_color": "grey",
      "car_type": "sedan",
      "private_parking_available": 1,
      "has_gps": 1,
      "has_air_conditioning": 1,
      "automatic_car": 0,
      "has_getaround_connect": 1,
      "has_speed_regulator": 0,
      "winter_tires": 0
    }]
  }'
```

**Response:**
```json
{"prediction": [147.9]}
```

### Python example

```python
import requests

response = requests.post(
    "https://marinedde-getaround-api.hf.space/predict",
    json={"input": [{
        "model_key": "Renault",
        "mileage": 50000,
        "engine_power": 120,
        "fuel": "diesel",
        "paint_color": "grey",
        "car_type": "sedan",
        "private_parking_available": 1,
        "has_gps": 1,
        "has_air_conditioning": 1,
        "automatic_car": 0,
        "has_getaround_connect": 1,
        "has_speed_regulator": 0,
        "winter_tires": 0
    }]}
)
print(response.json())  # {"prediction": [147.9]}
```

---

## Local Setup

### Requirements

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/marinedde/getaround.git
cd getaround
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Download the data

Place the files in the `data/` folder before running the notebook or training the model:

- [get_around_delay_analysis.xlsx](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx)
- [get_around_pricing_project.csv](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv)

### Train the model

```bash
python models/train.py
```

### Run the API

```bash
python -m uvicorn api.main:app --reload
# API available at http://127.0.0.1:8000
```

### Run the dashboard

```bash
python -m streamlit run streamlit_app/streamlit_app.py
# Dashboard available at http://localhost:8501
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Data Analysis | Python, Pandas, Plotly |
| Machine Learning | scikit-learn, GradientBoostingRegressor |
| API | FastAPI, Uvicorn, Pydantic |
| Dashboard | Streamlit, Plotly |
| Deployment | Docker, Hugging Face Spaces |
| Version Control | GitHub |

---

## Data

Datasets are not included in this repository. Download them and place them in the `data/` folder:

- [Delay Analysis](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx) — 21,310 rentals
- [Pricing Optimization](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv) — 4,843 cars

---

## Author

**Marine Deldicque**  
Jedha Bootcamp — CDSD 2026
