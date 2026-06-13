# Certification CDSD — Marine Deldicque

**RNCP35288 · Niveau 6 (BAC+4) · Jedha Bootcamp 2026**

Infirmière libérale reconvertie en data science, ce repository regroupe l'ensemble des projets réalisés pour la certification CDSD. Chaque projet correspond à un bloc de compétences — de la construction d'infrastructure de données jusqu'au déploiement en production, en passant par l'analyse exploratoire, le Machine Learning, le Deep Learning et la direction de projets data.

---

## Bloc 1 — Infrastructure de données

### Kayak · [`bloc1-kayak/`](bloc1-kayak/)

Construire un pipeline de données complet pour recommander les meilleures destinations de voyage en France, en croisant données météo et offre hôtelière sur 35 villes.

Le pipeline collecte les coordonnées GPS via l'API Nominatim, les prévisions météo sur 5 jours via OpenWeatherMap, et les données hôtelières via SerpAPI. Les données brutes sont stockées dans un Data Lake sur AWS S3, puis transformées et chargées dans un Data Warehouse MySQL sur AWS RDS. Les résultats sont visualisés sous forme de deux cartes interactives Plotly : les 5 meilleures destinations et les 20 meilleurs hôtels.

**Stack** : Python · Nominatim · OpenWeatherMap API · SerpAPI · AWS S3 · AWS RDS MySQL · Plotly · boto3 · SQLAlchemy

**Données** : [Coordonnées GPS Nominatim](https://nominatim.openstreetmap.org) · [Météo OpenWeatherMap](https://openweathermap.org/api)

---

## Bloc 2 — Analyse exploratoire et inférentielle

### Speed Dating · [`bloc2-speed-dating/`](bloc2-speed-dating/)

Analyse exploratoire d'un dataset issu d'expériences de speed dating pour identifier les facteurs déterminants dans la décision de revoir quelqu'un. Le projet couvre le nettoyage de données, les analyses univariées et multivariées, les tests statistiques d'indépendance et les visualisations des corrélations entre attributs physiques, comportementaux et socio-démographiques.

**Stack** : Python · Pandas · NumPy · Matplotlib · Seaborn · Plotly · SciPy

**Données** : [Speed Dating Dataset — Jedha](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/speed_dating.csv)

### Steam · [`bloc2-steam/`](bloc2-steam/)

Analyse de données massives issues de la plateforme Steam (jeux vidéo) pour comprendre les dynamiques du marché : genres dominants, corrélations entre prix et popularité, comportements des joueurs. Le projet utilise Databricks et PySpark pour traiter des volumes de données qui dépassent la capacité d'un environnement local.

**Stack** : Python · PySpark · Databricks · Pandas · Plotly · Seaborn

**Données** : [Steam Games Dataset — Jedha](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/steam.csv)

---

## Bloc 3 — Machine Learning supervisé et non supervisé

### Walmart Sales · [`bloc3-walmart/`](bloc3-walmart/)

Prédiction des ventes hebdomadaires de 45 magasins Walmart à l'aide d'algorithmes de régression. Le projet inclut une phase de feature engineering poussée (gestion des jours fériés, effets saisonniers, variables de lag) et une comparaison de plusieurs modèles — Linear Regression, Random Forest, XGBoost — avec cross-validation.

**Stack** : Python · Scikit-Learn · Pandas · NumPy · Plotly · XGBoost

**Données** : [Walmart Sales — Jedha](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/walmart_sales.csv)

### Conversion Rate · [`bloc3-conversion-rate/`](bloc3-conversion-rate/)

Prédiction du taux de conversion d'un site e-commerce à partir de données comportementales utilisateurs. Pipeline complet avec Scikit-Learn (preprocessing, classification supervisée), analyse de l'importance des variables, et optimisation du seuil de classification pour maximiser le F1-score.

**Stack** : Python · Scikit-Learn · Pandas · Plotly · Matplotlib

**Données** : [Conversion Rate Dataset — Jedha](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/conversion_rate.csv)

### North Face · [`bloc3-northface/`](bloc3-northface/)

Système de recommandation de produits basé sur les descriptions textuelles du catalogue North Face. Le projet combine NLP, clustering non supervisé sur texte et topic modeling. Les descriptions sont vectorisées avec TF-IDF (avec `max_df=0.4` pour éliminer les termes génériques de la marque), puis clusterisées via DBSCAN avec distance cosinus — ce qui donne 14 clusters thématiques bien définis (vestes alpines, sous-vêtements techniques, bagagerie, etc.). La fonction `find_similar_items()` retourne les 5 produits les plus proches depuis le même cluster. La décomposition LSA (TruncatedSVD) produit 15 topics avec 38.7% de variance expliquée.

**Stack** : Python · Scikit-Learn · DBSCAN · TF-IDF · TruncatedSVD · spaCy · WordCloud · Pandas

**Données** : [North Face Products — Jedha](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/northface.csv)

---

## Bloc 4 — Deep Learning

### AT&T Spam Detector · [`bloc4-spam-detector/`](bloc4-spam-detector/)

Détection automatique de SMS spam par réseaux de neurones profonds. Le projet couvre le prétraitement NLP (tokenisation, padding, encodage), la construction d'un réseau de neurones avec couche d'embedding entraînable, et une comparaison avec un modèle de transfer learning (DistilBERT via HuggingFace Transformers). Les métriques d'évaluation incluent accuracy, précision, recall et F1-score sur un jeu de test déséquilibré.

**Stack** : Python · TensorFlow / Keras · HuggingFace Transformers · NumPy · Scikit-Learn

**Données** : [SMS Spam Collection — UCI](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection)

---

## Bloc 5 — Industrialisation et déploiement

### Getaround · [`bloc5-getaround/`](bloc5-getaround/)

Déploiement d'une solution complète d'analyse et de prédiction de prix pour la plateforme Getaround (Airbnb des voitures). Le projet comprend deux livrables en production.

Le **dashboard Streamlit** aide le Product Manager à fixer un seuil minimum entre deux locations : 57.5% des conducteurs rendent la voiture en retard, 218 cas problématiques identifiés sur 21 310 locations. Un simulateur interactif permet de tester différents seuils et scopes. Recommandation : 120 minutes pour toutes les voitures — 67.4% des cas résolus pour seulement 3.1% de revenus impactés.

L'**API FastAPI** prédit le prix journalier optimal pour une voiture donnée. Le modèle (GradientBoostingRegressor, R²=0.756, RMSE=16€) est exposé via un endpoint `/predict` conteneurisé avec Docker et déployé sur Hugging Face Spaces.

| Service | Lien |
|---------|------|
| Dashboard Streamlit | https://huggingface.co/spaces/marinedde/getaround-dashboard |
| API FastAPI | https://huggingface.co/spaces/marinedde/getaround-api |
| Documentation Swagger | https://marinedde-getaround-api.hf.space/docs |

**Stack** : Python · FastAPI · Streamlit · Plotly · Scikit-Learn · Docker · Hugging Face Spaces

**Données** : [Delay Analysis](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx) · [Pricing Dataset](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv)

---

## Bloc 6 — Direction de projet data

### OncoPrint · [`bloc6-oncoprint/`](bloc6-oncoprint/)

Projet final de certification. Application de data science appliquée à l'oncologie, combinant exploration de données génomiques, modélisation prédictive et déploiement. Le projet mobilise l'ensemble des compétences de la formation : EDA, ML supervisé et non supervisé, NLP ou feature engineering avancé, architecture de données, visualisation Streamlit et déploiement FastAPI/Docker. Le background infirmier apporte une dimension clinique réelle à l'interprétation des résultats.

| Service | Lien |
|---------|------|
| Dashboard Streamlit | https://huggingface.co/spaces/marinedde/oncoprint-dashboard |
| API FastAPI | https://huggingface.co/spaces/marinedde/oncoprint-api |

**Stack** : Python · Scikit-Learn · FastAPI · Streamlit · MLflow · Docker · Pandas · Plotly

**Données** : [TCGA BRCA Multi-Omics — Kaggle](https://www.kaggle.com/datasets/samdemharter/brca-multiomics-tcga) · 705 patients · 1 941 features (RNA-seq, CNV, mutations, protéomique RPPA)

---

## Structure du repository

```
cdsd-certification/
├── README.md
├── bloc1-kayak/
│   └── kayak_data_pipeline.ipynb
├── bloc2-eda/
│   ├── speed-dating/
│   └── steam/
├── bloc3-machine-learning/
│   ├── walmart/
│   ├── conversion-rate/
│   └── northface/
├── bloc4-deep-learning/
│   └── spam-detector/
├── bloc5-deployment/
│   └── getaround/
│       ├── api/
│       ├── streamlit_app/
│       ├── models/
│       ├── notebooks/
│       └── data/
└── bloc6-final/
    └── oncoprint/
```

---

## Auteure

**Marine Deldicque**
Infirmière libérale (IDEL) · Data Scientist · Nouvelle-Calédonie
Jedha Bootcamp — Certification CDSD 2026
[GitHub](https://github.com/marinedde)
