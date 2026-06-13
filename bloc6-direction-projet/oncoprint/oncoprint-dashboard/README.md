---
title: OncoPrint Dashboard
emoji: 🧬
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: "1.33.0"
app_file: streamlit_app.py
pinned: false
license: mit
---

# 🧬 OncoPrint — Dashboard Clinique

**Dashboard Streamlit — Certification CDSD Jedha 2026 — Marine Deldicque**

---

## Description

Dashboard interactif de classification moléculaire du cancer du sein et de pronostic de survie, basé sur les données TCGA-BRCA.

## Pages

| Page | Description |
|------|-------------|
| 🏠 Accueil | Vue d'ensemble du projet et métriques clés |
| 🩺 Aide à la décision | Prédiction clinique guidée par profil |
| 🔬 Outil de recherche | Prédiction manuelle + batch CSV |
| 📚 Explorer & apprendre | Comprendre les sous-types moléculaires |
| ⏱️ Pronostic Survie | Courbes Kaplan-Meier + Hazard Ratios Cox PH |
| 📊 Performances | Métriques du modèle XGBoost |
| ℹ️ À propos | Contexte et stack technique |

## Stack

`Python 3.10` · `Streamlit` · `XGBoost` · `scikit-learn` · `lifelines` · `Plotly` · `HuggingFace Spaces`
