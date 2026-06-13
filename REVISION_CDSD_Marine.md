# Révision CDSD — Marine Deldicque
**Examen : 17 juin 2026 · Aujourd’hui : 3 juin → 14 jours de préparation**

Ce document t’aide à **maîtriser chaque projet de A à Z**, même si tu t’es beaucoup aidée des LLM. Chaque section : analogie → concepts → ton code → chiffres à retenir → Q/R jury.

---

## 1. Verdict global : est-ce que tu réponds à Jedha ?

| Bloc | Projet(s) | Conformité | À corriger avant le 17/06 |
|------|-----------|------------|---------------------------|
| **1** | Kayak | ✅ **OK** | Préparer 2 min sur **RGPD** (géoloc, APIs, consentement) |
| **2** | Speed Dating + Steam | ⚠️ **Partiel** | **URL Databricks publiée** pour Steam ; 2–3 **tests statistiques** pour Speed Dating |
| **3** | Walmart + Conversion + North Face | ⚠️ **Presque OK** | North Face : **14 vs 80 clusters** (aligner slide/code) ; Conversion : garder preuve soumission Kaggle |
| **4** | AT&T Spam | ✅ **OK** | Savoir expliquer embedding vs BERT |
| **5** | Getaround | ✅ **OK** | Réveiller les Spaces HF la veille ; démo curl `/predict` |
| **6** | OncoPrint | ✅ **OK** (slides PM/RGPD) | Cohérence métriques ; angle clinique IDEL |

**Conclusion : tu peux passer la certification.** Les livrables techniques sont là. Le risque principal n’est pas le code — c’est l’**oral** si tu ne peux pas expliquer *pourquoi* chaque choix (surtout après usage intensif de LLM).

### Format examen (à mémoriser)

| Bloc | Durée totale | Présentation | Q/R |
|------|--------------|--------------|-----|
| 1 à 5 | 10 min | 5 min | 5 min |
| 6 | 20 min | 10 min | 10 min |
| **Certif complète** | **1h10** | Tous les blocs **en une fois** | Dossier imprimé lu par le jury **avant** ta présentation |

**Bloc 2 jour J :** déposer **Speed Dating + Steam**, présenter **un seul** au choix.  
**Bloc 3 jour J :** déposer **les 3**, présenter **un seul** au choix.

---

## 2. Plan de révision 14 jours

| Jours | Focus | Action concrète |
|-------|--------|-----------------|
| 3–4 juin | Bloc 1 Kayak | Relire notebook + refaire schéma S3→RDS à la main |
| 5–6 juin | Bloc 2 | ~~chi² ajouté~~ ; Steam : **toi** → Publish Databricks + URL dans `bloc2_eda.txt` |
| 7–8 juin | Bloc 3 | Refaire pipeline Walmart ; Conversion F1 ; ~~North Face eps=0.6 fait~~ |
| 9 juin | Bloc 4 | Expliquer à voix haute embedding + DistilBERT |
| 10 juin | Bloc 5 | Tester dashboard + API + curl |
| 11–13 juin | Bloc 6 | Répéter soutenance OncoPrint (10 min chrono) |
| 14–15 juin | Mock oral | 5 min par bloc + Q/R avec quelqu’un |
| 16 juin | Logistique | Imprimer dossiers, réveiller HF Spaces |
| 17 juin | Examen | Arriver avec dossier + diapos |

---

## 3. Bloc 1 — Kayak (Infrastructure)

### Analogie
**Kayak = une cuisine de restaurant.**  
- **Collecte** = courses (marchés = APIs).  
- **Data Lake (S3)** = réserve (cartons bruts, pas encore prêts à servir).  
- **Data Warehouse (RDS)** = cuisine organisée (ingrédients étiquetés, tables SQL).  
- **Cartes Plotly** = menu du jour pour le marketing.

### Compétences Jedha couvertes
| Compétence | Ton implémentation |
|------------|-------------------|
| Collecte multi-sources | Nominatim + OpenWeather + SerpAPI |
| Data Lake | S3 `kayak-project-marine/raw/` |
| ETL | Pandas → nettoyage → MySQL RDS |
| Big Data (mention) | README : évolution Spark/Redshift |
| RGPD | À verbaliser (pas seulement dans le code) |

### Pipeline (à redessiner sans aide)

```
35 villes → Nominatim (lat/lon)
         → OpenWeather (5 jours, score météo)
         → SerpAPI google_hotels (20 hôtels/ville = 700)
         → CSV → S3 (lake)
         → ETL → RDS : cities, weather, hotels
         → Plotly : top 5 destinations + top 20 hôtels
```

### Code / concepts essentiels

**Nominatim** : géocodage gratuit OSM. `User-Agent` obligatoire + `sleep(1)` = respect du serveur (équivalent « ne pas spammer la caisse »).

**Score météo (exemple)** : `avg_temp - total_rain - (avg_humidity/10)` — *ta* définition du « beau temps ». Le jury peut demander : « Pourquoi pas uniquement la pluie ? » → Réponse : critère métier marketing, documenté.

**SerpAPI vs Booking scrape** : Booking bloque bots (Cloudflare). SerpAPI = interface stable vers Google Hotels → **conforme** au brief Jedha.

**S3 vs RDS** :
- S3 = fichiers immuables, cheap, historique brut.
- RDS = requêtes SQL, jointures, équipes métiers.

### Chiffres à retenir
- 35 villes, 700 hôtels, 3 tables RDS
- 2 cartes : **5** destinations, **20** hôtels

### Q/R jury — Bloc 1

**Q : C’est quoi un Data Lake vs Data Warehouse ?**  
**R :** Le lake stocke tout brut (CSV S3). Le warehouse structure pour l’analyse (MySQL, schéma, types, clés). On ETL du lake vers le warehouse.

**Q : RGPD sur ce projet ?**  
**R :** Données agrégées villes/hôtels publics ; pas de données personnelles utilisateurs Kayak. Respect robots.txt / quotas APIs ; clés en secrets (Colab), pas dans Git. Pour une app réelle : base légale, minimisation, durée de conservation, droit d’accès.

**Q : Pourquoi pas Spark ici ?**  
**R :** Volume modeste (35×20). Spark utile si millions de lignes ou flux temps réel — évolution possible (Redshift, Kafka dans README).

**Q : Montre-moi une requête SQL utile.**  
**R :** `SELECT city, weather_score FROM weather ORDER BY weather_score DESC LIMIT 5;` + jointure hotels sur city_id.

---

## 4. Bloc 2 — Speed Dating (présentation probable)

### Analogie
**Speed dating = un entretien d’embauche en 4 minutes.** Chaque ligne = une rencontre. `match=1` seulement si **les deux** disent oui (`dec` ET `dec_o`).

### Dataset
- ~8 378 interactions, 551 participants, 2002–2004
- **Taux de match global : 16,5 %**
- Hommes acceptent plus souvent → goulot = sélectivité féminine

### Analyses que tu as faites
- Nettoyage, stats descriptives, corrélations **Pearson** avec `dec` / `match`
- Comparaisons hommes/femmes, critères (attr, sinc, intel…)
- Intérêts communs vs même race (taux de match proches → aucun seul ne « prédit » bien)

### Gap : tests inférentiels
Jedha cite « analyses inférentielles ». Tu as surtout de l’**exploratoire**. Avant l’examen, ajoute par exemple :

```python
from scipy.stats import chi2_contingency
# Match vs genre du décideur
table = pd.crosstab(df['gender'], df['match'])
chi2, p, dof, expected = chi2_contingency(table)
# Si p < 0.05 → association significative
```

Ou test Mann-Whitney : notes `attr` match=1 vs match=0.

**Si tu n’ajoutes pas le code** : dis au jury « hypothèses exploratoires ; pour causalité il faudrait modèles multivariés et attention au biais de sélection ».

### Q/R jury — Speed Dating

**Q : Pourquoi Pearson ?**  
**R :** Mesure liaison **linéaire** entre deux variables quantitatives. Pas de causalité.

**Q : Attractivité déclarée vs réelle ?**  
**R :** Les gens surévaluent parfois ce qu’ils recherchent vs ce qui corrèle au match — écart « préférences déclarées / comportement réel ».

**Q : Premier ou dernier rendez-vous de la soirée ?**  
**R :** Préparer une analyse par `order` ou vague si colonne dispo — effet fatigue / standards qui baissent.

---

## 5. Bloc 2 — Steam (dépôt obligatoire, présentation possible)

### Analogie
**Steam = analyser tout le catalogue Netflix des jeux vidéo**, mais le fichier est trop gros pour Excel → **PySpark = plusieurs caissiers en parallèle**.

### Technique
- Notebook format **Databricks**
- `spark.read.csv`, schéma imbriqué, `groupBy`, `explode`, `getField`
- ~27 075 jeux

### Gap critique
**URL notebook publié Databricks** — obligatoire pour le jury. Bouton **Publish** → copier l’URL dans `Marine_Deldicque_CDSD_liens/bloc2_eda.txt`.

### Q/R jury — Steam

**Q : Pourquoi Spark ?**  
**R :** Données semi-structurées JSON volumineuses ; transformations distribuées ; même code scalable cluster.

**Q : Différence Pandas vs Spark ?**  
**R :** Pandas = une machine, tout en RAM. Spark = lazy evaluation, partitions, fault tolerance.

---

## 6. Bloc 3 — Walmart (régression)

### Analogie
**Prédire les ventes = prévoir la taille d’une récolte** en fonction de météo (température), prix carburant (engrais), chômage (moral des clients), magasin (terre), vacances (saison).

### Pipeline Jedha
1. EDA + viz  
2. **LinearRegression** (baseline)  
3. **Ridge / Lasso** (régularisation) + GridSearchCV optionnel

### Prétraitements importants (à savoir réciter)
- Supprimer lignes où **Weekly_Sales** manquant (jamais imputer la cible)
- Feature engineering **Date** → year, month, day, day_of_week
- Outliers : valeurs hors [μ−3σ, μ+3σ] sur Temp, Fuel_Price, CPI, Unemployment
- Catégorielles : Store, IsHoliday — numériques scalées

### Tes résultats (test set)

| Modèle | RMSE test | R² test |
|--------|-----------|---------|
| LinearRegression | ~188 478 $ | **0,8977** |
| Ridge (α=1) | ~216 126 $ | 0,8655 |
| Lasso (α=1) | ~188 476 $ | **0,8977** |

**Lecture :** Train R² ~0,98 vs test ~0,90 → léger overfitting ; Ridge réduit l’écart train/test mais R² test un peu plus bas ici.

### Concepts

**RMSE** : erreur moyenne en dollars (pénalise gros écarts).  
**R²** : part de variance expliquée (1 = parfait, 0 = inutile).  
**Ridge** : pénalise L2, rétrécit coefficients, garde toutes les variables.  
**Lasso** : L1, peut mettre des coefs à **0** → sélection de variables.

### Q/R jury — Walmart

**Q : Coefficient positif sur Temperature ?**  
**R :** +1°C associé à +X $ de ventes *toutes choses égales* — corrélation, pas causalité directe.

**Q : Pourquoi GridSearchCV ?**  
**R :** Cherche le meilleur hyperparamètre (ex. `alpha` Ridge) par validation croisée, limite overfitting sur le choix d’alpha.

---

## 7. Bloc 3 — Conversion Rate (classification déséquilibrée)

### Analogie
**Newsletter = pêche à la ligne.** Peu de poissons mordent (`converted=1`). Si tu dis « personne ne convertit », accuracy haute mais **tu rates tous les vrais clients**.

### Métrique officielle : F1-score

\[
F1 = 2 \cdot \frac{precision \cdot recall}{precision + recall}
\]

- **Precision** : parmi tes « oui », combien sont vrais ?  
- **Recall** : parmi les vrais convertis, combien as-tu trouvés ?

**Pourquoi pas accuracy ?** Classes déséquilibrées → modèle trivial « toujours 0 » peut avoir ~90 % accuracy et F1 ≈ 0.

### Pipeline
1. EDA (sample 10k pour viz)  
2. Baseline LogisticRegression (1 variable : `total_pages_visited`) ~F1 0,51  
3. RandomForest + **GridSearchCV scoring='f1'**  
4. Prédictions `conversion_data_test_predictions_[nom].csv`

### Code pattern à comprendre

```python
# MÊME métrique que le leaderboard
f1_score(y_true, y_pred)

# GridSearch optimise F1, pas accuracy
GridSearchCV(..., scoring='f1')

# fit sur train, transform sur test — PAS fit_transform sur test !
scaler.transform(X_test)
```

### Q/R jury — Conversion

**Q : Levier métier si `new_user` important ?**  
**R :** Cibler onboarding nouveaux visiteurs, pages d’aide, A/B test parcours.

**Q : data_train vs data_test Kaggle ?**  
**R :** Train a la cible ; test non — évaluation indépendante anti-triche.

---

## 8. Bloc 3 — North Face (NLP non supervisé)

### Analogie
**Catalogue = bibliothèque sans rayons.** TF-IDF = fiche par livre ; **DBSCAN** = regrouper livres proches ; **LSA** = thèmes cachés (montagne, ski, ville…).

### Partie 1 — Clustering DBSCAN
- Nettoyage spaCy (stop words, lemmatisation)
- **TF-IDF** `max_df=0.4` → enlève mots trop fréquents (« north », « face »)
- **Distance cosinus** (standard texte)
- **DBSCAN** : `eps` = voisinage, `min_samples` = densité minimale

**Problème actuel :** tuning dit `eps=0.6 → 14 clusters ✅` mais `EPS_FINAL = 0.40 → 80 clusters`.  
**Action :** passer `EPS_FINAL = 0.6` OU corriger slides/README.

### Partie 2 — Recommandation

```python
def find_similar_items(item_id):
    # même cluster_id → top 5 autres produits
```

### Partie 3 — LSA (TruncatedSVD)
- Réduction dimension ; **variance expliquée ~38,7 %**
- Un document peut avoir plusieurs thèmes ; tu prends le thème dominant pour simplifier

### Q/R jury — North Face

**Q : DBSCAN vs KMeans ?**  
**R :** DBSCAN trouve forme arbitraire + outliers ; KMeans suppose clusters sphériques, k fixé.

**Q : Pourquoi cosinus sur TF-IDF ?**  
**R :** On compare l’**angle** entre vecteurs (profil de mots), pas la longueur absolue.

---

## 9. Bloc 4 — AT&T Spam (Deep Learning)

### Analogie
**SMS = phrases courtes.**  
- **Modèle 1 (Embedding + Dense)** : apprendre un dictionnaire de « sens » mot par mot sur *tes* 5k SMS.  
- **DistilBERT** : embaucher un polyglotte déjà formé sur Internet, fine-tuner sur spam.

### Modèle simple (Keras)
1. Tokenizer → séquences d’entiers  
2. `Embedding` (vecteur par mot)  
3. GlobalAveragePooling1D  
4. Dense + sigmoid (binaire)

### Transfer learning
- Tokenizer HuggingFace + DistilBERT  
- Fine-tuning 2 epochs  
- Meilleure généralisation, peu de données

### Tes métriques (test)

| Modèle | Accuracy | F1 spam |
|--------|----------|---------|
| Embedding + Dense | ~0,979 | ~0,919 |
| DistilBERT | ~0,987 | ~0,950 |

**Classes déséquilibrées** → regarder **recall spam** (ne pas rater un spam).

### Q/R jury — Bloc 4

**Q : Pourquoi padding ?**  
**R :** Batch = matrices rectangulaires ; SMS de longueurs différentes → même longueur max.

**Q : Overfitting signes ?**  
**R :** Train accuracy >> test ; early stopping, dropout, plus de données, BERT.

**Q : GAN / données synthétiques ?**  
**R :** Compétence bloc 4 Jedha ; pas obligatoire sur AT&T — tu peux mentionner comme évolution.

---

## 10. Bloc 5 — Getaround (Déploiement)

### Analogie
**Getaround = aéroport de location.**  
- **Streamlit** = tour de contrôle (retards, seuils).  
- **API /predict** = calculateur de prix automatique.  
- **Docker + HF** = boutique ouverte 24/7 sur Internet.

### Partie analyse retards (dashboard)
Chiffres clés :
- **21 310** locations  
- **57,5 %** retours en retard  
- **218** cas problématiques (chaîne de réservations)  
- Recommandation **120 min** entre locations : **67,4 %** cas résolus, **3,1 %** revenus impactés

### Partie ML prix
- **GradientBoostingRegressor**  
- **R² = 0,756**, **RMSE = 16 €** (test)

### API (à démontrer)

```bash
curl -i -H "Content-Type: application/json" -X POST \
  -d '{"input": [{"model_key":"...", "mileage":100, ...}]}' \
  https://marinedde-getaround-api.hf.space/predict
```

Réponse : `{"prediction": [prix_jour]}`  
Documentation : `/docs` (Swagger)

### MLflow / Docker
- Docker = boîte avec Python + modèle `.pkl` identique partout  
- MLflow = suivi expériences (si utilisé dans notebook)

### Q/R jury — Bloc 5

**Q : Seuil 120 min pour toutes les voitures ou Connect only ?**  
**R :** Mon analyse compare scénarios dans le simulateur Streamlit ; recommandation basée compromis revenus / satisfaction.

**Q : Différence FastAPI vs Flask ?**  
**R :** FastAPI : typage Pydantic, doc auto OpenAPI, async — idéal ML APIs.

---

## 11. Bloc 6 — OncoPrint (Direction de projet)

### Analogie
**OncoPrint = traducteur médical pour tumeurs.** Entrée = langage génomique (RNA, protéines). Sortie = sous-type + pronostic — comme un IDEL qui lit un dossier et oriente vers le bon parcours de soins (*sans remplacer le médecin*).

### Problème métier
4 sous-types moléculaires sein → traitements différents (hormonothérapie, Herceptin, chimio…).

### Données
- TCGA-BRCA public (recherche)  
- 705 → **536** patientes après nettoyage  
- **1936** features multi-omiques  
- Cible construite depuis ER / PR / HER2

### Cycle de vie (à raconter en 10 min)

1. **Cadrage** : enjeu clinique, RGPD données recherche publiques anonymisées  
2. **EDA** : déséquilibre classes, missing omiques  
3. **Preprocessing** : scaling, sélection features  
4. **Modélisation** : XGBoost + GridSearch ; attention **SMOTE** → tu as corrigé le leakage avec pipeline imbriqué (point fort oral)  
5. **Interprétation** : SHAP cohérent clinique (ER, HER2…)  
6. **Survie** : Kaplan-Meier + Cox PH (HR Triple Négatif ~2,31× vs Luminal A)  
7. **Industrialisation** : Streamlit + FastAPI + Docker sur HF  
8. **Limites** : pas un outil diagnostic ; Luminal B F1=0,50 ; petit n HER2

### Métriques (README — à savoir défendre)

| Métrique | Valeur |
|----------|--------|
| Accuracy test | 84,3 % |
| F1 macro | 76,3 % |
| CV 5-fold | 71,5 % ± 2,5 % |

**Si jury demande écart notebook/README :** plusieurs splits / SMOTE / holdout — la CV corrigée 71,5 % est l’estimation la plus honnête généralisation.

### Q/R jury — Bloc 6

**Q : Cahier des charges / budget / planning ?**  
**R :** Utiliser ta soutenance v5 : phases discovery, POC, MVP, déploiement ; budget cloud HF gratuit + temps équipe.

**Q : RGPD santé ?**  
**R :** TCGA = données recherche consenties, anonymisées ; pas de données patients NC en production ; disclaimer « aide à la décision recherche » ; pas de diagnostic auto.

**Q : Pourquoi Cox ?**  
**R :** Modèle survie avec censure (patiente perdue de vue) ; hazard ratio interprétable pour le jury médical.

**Q : Ton avantage IDEL ?**  
**R :** Pont entre biomarqueurs, parcours patient et communication médecin — crédibilité sur SHAP et limites cliniques.

---

## 12. Glossaire express (tous blocs)

| Terme | Une phrase |
|-------|------------|
| ETL | Extract → Transform → Load |
| Fit vs transform | Fit = apprendre sur train ; transform = appliquer sur test |
| Overfitting | Modèle apprend le bruit du train, mal sur nouveau |
| Cross-validation | Plusieurs découpes train/val pour estimer perf réelle |
| F1 | Compromis precision/recall |
| Embedding | Mot → vecteur de nombres capturant sens |
| API REST | URL + méthode HTTP + JSON |
| RGPD | Limiter, justifier, sécuriser données personnelles |

---

## 13. Checklist veille d’examen (16 juin)

- [ ] Dossiers projets **imprimés**
- [ ] Diapos **v2/v3/v5** à jour (pas `pptx ancien/`)
- [ ] URL Databricks Steam dans lien bloc 2
- [ ] North Face : 14 clusters cohérents slide/code
- [ ] HuggingFace : ouvrir dashboard + API Getaround et OncoPrint (réveiller)
- [ ] Tester `curl /predict` et `/docs`
- [ ] Préparer choix présentation bloc 2 et 3 (Speed Dating vs Steam ? Conversion vs North Face ?)
- [ ] 30 secondes d’intro par bloc : problème → données → méthode → résultat chiffré → limite

---

## 14. Script d’intro 30 s par bloc (à personnaliser)

**Bloc 1 :** « Pipeline Kayak : 35 villes, APIs météo et hôtels, lake S3, warehouse MySQL, deux cartes pour le marketing. »

**Bloc 2 :** « Speed Dating : 16,5 % de match ; facteurs corrélés au oui mutuel. » OU « Steam : PySpark sur 27k jeux pour tendances marché. »

**Bloc 3 :** « Walmart R² 0,90 ; Conversion optimisée F1 ; North Face recommandation par clustering texte. »

**Bloc 4 :** « Spam SMS : CNN simple puis DistilBERT, F1 spam 0,95. »

**Bloc 5 :** « Getaround : dashboard seuil 120 min, API prix en prod HF. »

**Bloc 6 :** « OncoPrint : sous-type sein depuis omiques TCGA, SHAP + survie + déploiement. »

---

*Bonne certification — tu as déjà fait le plus dur (les projets). Ces 14 jours servent à **posséder** ton discours.*

---

## Vidéos démo Getaround / OncoPrint

Guide détaillé (scripts minute par minute, CI/CD optionnel) : **`VIDEO_DEMOS_CDSD.md`**
