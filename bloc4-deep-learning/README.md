# AT&T Spam Detector (Bloc 4 · Deep Learning sur données non structurées)

Détection automatique de SMS frauduleux (spam) à partir du **texte seul**, par deux approches de
deep learning comparées à données strictement égales :

| | Modèle 1 : réseau simple (baseline) | Modèle 2 : DistilBERT (transfer learning) |
|---|---|---|
| Représentation du texte | Embedding appris de zéro (10 000 mots × 32 dims) | Embeddings contextuels pré-entraînés (Transformer) |
| Architecture | Embedding, moyenne des mots, Dense 64 ReLU, Dropout, sigmoïde | DistilBERT + tête de classification (2 logits) |
| Fonction de coût | Entropie croisée binaire, classe spam pondérée ×6,9 | Entropie croisée |
| Paramètres / entraînement | 0,32 M · ~2 s sur CPU | 67 M · ~3 min sur Apple Silicon (~1 min sur GPU T4) |

## Résultats (jeu de test : 1 034 SMS, dont 131 spams)

| Métrique | Réseau simple | DistilBERT fine-tuné |
|---|---|---|
| Précision spam | 0,899 | **0,992** |
| Rappel spam | 0,947 | 0,947 |
| **F1 spam** | 0,922 | **0,969** |
| Accuracy | 0,980 | 0,992 |
| Messages légitimes bloqués à tort (FP) | 14 | **1** |
| Spams manqués (FN) | 7 | 7 |

Le gain du transfer learning (+0,047 de F1 spam) porte sur la **précision** : à rappel égal,
DistilBERT divise par 14 le nombre de vrais messages bloqués, l'erreur la plus coûteuse pour le client.
Sous contrainte de précision ≥ 98 % (seuil réglé sur la validation), le réseau simple s'effondre
(rappel 0,27) alors que DistilBERT conserve un rappel de 0,947.

## Méthodologie

- **Données** : [SMS Spam Collection (UCI)](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection),
  5 572 SMS étiquetés ham / spam. **403 doublons retirés** avant le découpage (sinon fuite du train vers le test).
- **Découpage stratifié** train 3 721 / validation 414 / test 1 034. La validation sert à l'early
  stopping, au choix de l'epoch et au réglage du seuil ; le test n'est utilisé qu'une fois, à la fin.
- **Métrique de référence** : F1 de la classe spam (classes déséquilibrées 87 / 13).
- **Pipeline NLP (modèle 1)** : nettoyage, tokenisation (vocabulaire ajusté sur le train uniquement),
  padding à 64 jetons. **DistilBERT** reçoit le texte brut : son tokenizer WordPiece exploite
  chiffres et ponctuation, qui sont des signaux de spam.
- **Analyses complémentaires** : mots caractéristiques de chaque classe, plus proches voisins et
  projection PCA des embeddings appris, courbes précision / rappel, choix du seuil, analyse des erreurs.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `ATTspamdetector.ipynb` | Notebook complet, exécuté (sorties et figures incluses) |
| `ATT_SpamDetector_Presentation.pptx` | Support de soutenance (10 slides) |
| `requirements.txt` | Dépendances Python |

## Reproduire

```bash
pip install -r requirements.txt
jupyter notebook ATTspamdetector.ipynb
```

Le jeu de données est téléchargé automatiquement si `spam.csv` est absent. Le notebook s'exécute
tel quel sur Google Colab (GPU T4 recommandé pour le fine-tuning) ou en local (CPU / Apple Silicon).
Les graines aléatoires sont fixées (`SEED = 42`) ; de légères variations restent possibles selon le matériel.
