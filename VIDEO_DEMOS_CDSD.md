# Vidéos de démo — Getaround & OncoPrint

**Marine Deldicque · CDSD · Examen 17 juin 2026**

---

## Ce que Jedha exige vraiment (pas de vidéo obligatoire)

| Bloc | Livrable officiel | Vidéo ? |
|------|-------------------|---------|
| **5 Getaround** | Dashboard **en ligne**, API `/predict`, page `/docs`, code GitHub, Docker | Non imposée — **démo live** ou captures suffisent à l’oral |
| **6 OncoPrint** | Projet final : slides + **démonstration du produit** à l’oral / Demoday | Souvent une **courte démo écran** dans la présentation (2–3 min), pas un film documentaire |

**CI/CD (GitHub Actions)** : **pas demandé** pour la certification CDSD bloc 5. C’est un **plus** pour montrer que tu industrialises (bonus bloc 5 « standardiser l’environnement »). Ne confonds pas avec le livrable principal : **Streamlit + FastAPI + Hugging Face**.

---

## Quelles vidéos faire (recommandation)

| # | Projet | Durée | Priorité | Pour qui |
|---|--------|-------|----------|----------|
| 1 | Getaround — Dashboard Streamlit | 3–4 min | **Haute** | Jury bloc 5 + dossier |
| 2 | Getaround — API `/predict` + `/docs` | 2 min | **Haute** | Jury bloc 5 |
| 3 | OncoPrint — Dashboard Streamlit | 4–5 min | **Haute** | Jury bloc 6 (10 min présentation) |
| 4 | OncoPrint — Parcours clinique complet | 2 min | Moyenne | Soutenance / portfolio |
| 5 | Getaround — Déploiement Docker → HF | 3 min | Basse (bonus) | Si on te pose des questions déploiement |
| 6 | CI/CD GitHub Actions | 2 min | **Optionnel** | Seulement si tu as mis en place un workflow (voir § CI/CD) |

**Total utile : ~10–12 minutes** de contenu bien découpé (mieux que une vidéo de 20 min).

---

## Outils d’enregistrement (Mac)

| Outil | Usage |
|-------|--------|
| **QuickTime** | Fichier → Nouvel enregistrement écran → micro interne |
| **Cmd + Shift + 5** | Capture vidéo macOS intégrée |
| **Loom** | Partage lien rapide pour le jury / Jedha |
| **OBS** | Si tu veux flouter onglets / notifications |

**Réglages :** 1920×1080 ou 1280×720, parler lentement, agrandir le navigateur (125 %).

---

## Vidéo 1 — Getaround Streamlit (script 3–4 min)

**URL :** https://huggingface.co/spaces/marinedde/getaround-dashboard  
**Avant :** ouvrir l’URL 1 min avant (réveiller le Space).

### Script minute par minute

| Temps | Action | Phrase à dire (exemple) |
|-------|--------|-------------------------|
| 0:00 | Page d’accueil / Vue générale | « Dashboard pour le Product Manager : retards entre deux locations. » |
| 0:30 | KPIs | « 57,5 % des conducteurs rendent en retard ; 218 cas problématiques sur les locations enchaînées. » |
| 1:00 | Analyse des retards | Montrer histogramme / mobile vs Connect | « Le check-in mobile est plus risqué que Connect. » |
| 1:45 | **Simulateur de seuil** | Bouger le slider à 60, 120, 180 | « À 120 minutes, 67,4 % des cas résolus pour 3,1 % de revenus impactés — notre recommandation. » |
| 2:30 | Prédiction de prix | Remplir le formulaire, lancer prédiction | « Le dashboard appelle l’API ML pour suggérer un prix journalier. » |
| 3:15 | Conclusion | — | « Deux livrables : analyse métier + API pricing en production sur Hugging Face. » |

**Fichier à montrer si question code :** `bloc5-deployment/getaround/streamlit_app/streamlit_app.py` (pages sidebar, `compute_analysis`, appel `requests.post` vers l’API).

---

## Vidéo 2 — Getaround API (script 2 min)

**URLs :**  
- API : https://marinedde-getaround-api.hf.space  
- Docs : https://marinedde-getaround-api.hf.space/docs  

| Temps | Action |
|-------|--------|
| 0:00 | Ouvrir `/docs` Swagger — montrer POST `/predict` |
| 0:30 | « Try it out » avec un JSON exemple OU terminal |
| 1:00 | Coller commande curl (README) → montrer `{"prediction": [147.9]}` |
| 1:30 | Montrer `api/main.py` : FastAPI, Pydantic, `joblib.load` |
| 1:45 | Montrer `api/Dockerfile` : image Python, `uvicorn` port 7860 |

**Commande curl à avoir sous la main :**

```bash
curl -X POST "https://marinedde-getaround-api.hf.space/predict" \
  -H "Content-Type: application/json" \
  -d '{"input":[{"model_key":"Renault","mileage":50000,"engine_power":120,"fuel":"diesel","paint_color":"grey","car_type":"sedan","private_parking_available":1,"has_gps":1,"has_air_conditioning":1,"automatic_car":0,"has_getaround_connect":1,"has_speed_regulator":0,"winter_tires":0}]}'
```

---

## Vidéo 3 — OncoPrint Streamlit (script 4–5 min)

**URL :** https://huggingface.co/spaces/marinedde/oncoprint-dashboard  
**Avant :** réveiller aussi https://marinedde-oncoprint-api.hf.space (le dashboard appelle l’API).

### Pages à enchaîner (sidebar)

| Temps | Section | Message clé |
|-------|---------|-------------|
| 0:00 | Accueil | « OncoPrint : sous-type moléculaire sein à partir de données TCGA, outil d’aide — pas un diagnostic. » |
| 0:45 | Aide à la décision | Sliders biomarqueurs OU profil prédéfini « Triple Négatif » |
| 1:30 | Lancer prédiction | Montrer sous-type + probabilités + confiance |
| 2:15 | Survie | Kaplan-Meier / HR vs Luminal A (TN ~2,31×) |
| 3:00 | SHAP ou top features | « Cohérent clinique : ER pour Luminal A, HER2 pour HER2-enriched. » |
| 3:45 | Rapport Claude (si activé) | « Vulgarisation pour un public médical — option GenAI. » |
| 4:30 | Métriques / limites | « Accuracy 84 %, Luminal B plus difficile, données recherche TCGA. » |

**Code à citer :** `bloc6-direction-projet/oncoprint/oncorint-dashboard/streamlit_app.py` — `API_URL`, `requests.post(.../predict)`.

---

## Vidéo 4 — OncoPrint API (optionnel, 2 min)

**URL docs :** https://marinedde-oncoprint-api.hf.space/docs  

- GET `/health` — modèle chargé  
- POST `/predict` — JSON minimal avec `rs_ESR1`, `pp_ER.alpha`, etc.  
- GET `/survival/Triple%20N%C3%A9gatif`  

---

## CI/CD — faut-il une vidéo ?

**Non pour valider le CDSD.** Si tu veux quand même une vidéo « industrialisation » :

1. Montrer **Dockerfile** → build local → image  
2. Montrer **Hugging Face Spaces** : repo lié à GitHub, rebuild au push  
3. *(Optionnel)* GitHub Actions qui vérifie que l’API démarre

Un workflow minimal peut vivre dans `.github/workflows/getaround-smoke.yml` (voir repo si ajouté).

**Script vidéo CI/CD (2 min) :**  
« À chaque push sur `main`, GitHub Actions installe les deps et vérifie que `api/main.py` charge le modèle — pas de déploiement automatique, le déploiement reste sur Hugging Face. »

---

## Où déposer les vidéos

| Destination | Usage |
|-------------|--------|
| Lien dans **soutenance OncoPrint** (slide « Démo ») | Bloc 6 |
| **Marine_Deldicque_CDSD_liens** (fichier texte avec URLs Loom/YouTube non listés) | Jury |
| Portfolio LinkedIn / GitHub README | Après certification |
| **Pas obligatoire** dans le zip GitHub Jedha | Sauf consigne de ta promo |

---

## Checklist avant d’enregistrer

- [ ] Fermer notifications (Ne pas déranger)
- [ ] Réveiller les 3 Spaces (dashboard Getaround, API Getaround, dashboard + API OncoPrint)
- [ ] Script imprimé ou second écran
- [ ] Tester curl Getaround une fois
- [ ] OncoPrint : tester un profil prédéfini (évite sliders vides)
- [ ] Parler en français, termes techniques en anglais si le jury les utilise (F1, API, endpoint)

---

## À l’oral le 17 juin (sans vidéo)

Si pas le temps d’enregistrer : **démo live** identique aux scripts ci-dessus. La vidéo sert surtout à **répéter** sans stress et à laisser un lien au jury.

---

*Dernière mise à jour : correctifs repo (North Face eps=0.6, Speed Dating chi², lien Databricks Steam à compléter).*
