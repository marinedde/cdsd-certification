# 🛶 Projet Kayak — Pipeline de données

**Certification CDSD · Bloc 1 — Infrastructure de données**

Construire un pipeline de données complet pour recommander les meilleures destinations de voyage en France, en croisant données météo et offre hôtelière pour 35 villes.

---

## 🏗 Architecture

```
APIs (Nominatim · OpenWeatherMap · SerpAPI)
        ↓
  Data Lake (AWS S3)  ←— fichiers CSV bruts
        ↓
      ETL (Pandas · boto3)
        ↓
 Data Warehouse (AWS RDS MySQL)  ←— 3 tables nettoyées
        ↓
  Visualisations (Plotly)  ←— 2 cartes interactives
```

---

## 📋 Étapes du pipeline

| Étape | Outil | Description |
|-------|-------|-------------|
| 1. GPS | Nominatim (OSM) | Géocodage des 35 villes françaises |
| 2. Météo | OpenWeatherMap API | Prévisions 5 jours + calcul du score météo |
| 3. Hôtels | SerpAPI (Google Hotels) | 20 hôtels par ville = 700 hôtels au total |
| 4. Data Lake | AWS S3 | Stockage des CSV bruts dans `raw/` |
| 5. ETL | Pandas + SQLAlchemy | Nettoyage, transformation, chargement RDS |
| 6. Visualisation | Plotly | 2 cartes interactives (destinations + hôtels) |

---

## 🗂 Structure du projet

```
projet_kayak/
├── kayak_data_pipeline.ipynb   # Notebook principal (pipeline complet)
├── .gitignore
└── README.md
```

---

## ⚙️ Prérequis

### Secrets Colab (à configurer dans Colab > Secrets)

| Nom du secret | Description |
|--------------|-------------|
| `OWM_API_KEY` | Clé API OpenWeatherMap |
| `AWS_ACCESS_KEY_ID` | Clé d'accès AWS |
| `AWS_SECRET_ACCESS_KEY` | Clé secrète AWS |
| `RDS_PASSWORD` | Mot de passe AWS RDS MySQL |
| `SERPAPI_KEY` | Clé API SerpAPI |

> ⚠️ Les credentials ne sont jamais stockés en dur dans le code. Tout passe par les Secrets Colab (`userdata.get()`).

### Dépendances Python

```python
!pip install boto3 sqlalchemy pymysql plotly google-search-results
```

---

## 🚀 Lancer le notebook

1. Ouvrir `kayak_data_pipeline.ipynb` dans Google Colab
2. Configurer les 5 secrets dans **Colab > Secrets**
3. Exécuter toutes les cellules dans l'ordre (`Exécution > Tout exécuter`)

Le pipeline tourne en ~15 minutes (collecte météo + hôtels incluses).

---

## 📊 Résultats

**Score météo** : `avg_temp - total_rain - (avg_humidity / 10)`

Favorise les destinations chaudes et peu pluvieuses sur 5 jours de prévisions.

**Carte 1** — Top 5 destinations météo (bulles proportionnelles au score, couleur = température)

**Carte 2** — Top 20 hôtels dans ces 5 destinations (triés par `overall_rating` SerpAPI)

---

## ☁️ Infrastructure AWS

| Service | Usage |
|---------|-------|
| **S3** (`kayak-project-marine`) | Data Lake — stockage brut `raw/` |
| **RDS MySQL** (`kayak-db`) | Data Warehouse — 3 tables relationnelles |

Tables RDS : `cities` (35 lignes) · `weather` (35 lignes) · `hotels` (700 lignes)

---

## 📈 Passage à l'échelle (Big Data)

À l'échelle mondiale (millions d'hôtels, temps réel) :

| Besoin | Outil actuel | Outil à l'échelle |
|--------|-------------|-------------------|
| Traitement distribué | Pandas | Apache Spark (PySpark) |
| Data Warehouse analytique | RDS MySQL | Amazon Redshift |
| Exécution managée | Colab | Amazon EMR |
| Ingestion temps réel | Batch | Apache Kafka |

L'architecture Sources → Lake → ETL → Warehouse → Visu reste identique.

---

## 🔒 Bonnes pratiques

- Credentials gérés via **Secrets Colab** — jamais en dur dans le code
- Rate limiting respecté sur toutes les APIs (`time.sleep()`)
- Séparation **Data Lake** (brut) / **Data Warehouse** (nettoyé)
- Vérification du pipeline via requêtes SQL avec `JOIN`
- `rootkey.csv` exclu du repo via `.gitignore`

---

*Projet réalisé dans le cadre de la certification CDSD — Jedha Bootcamp*
