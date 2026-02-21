# -Backtest-SMA-AAPL-2020-2023

L'objectif de ce projet est d'évaluer la performance d'une stratégie de trading basée sur le croisement de moyennes mobiles simples (SMA) appliquée à l'action Apple (AAPL) entre 2020 et 2023.

## Aperçu des résultats

### 1. Signaux d'achat et de vente
Voici les points d'entrée et de sortie générés par l'algorithme :
![Signaux de Trading](Graph%20Stratégie%20SMA%20sur%20AAPL.png)

### 2. Performance Cumulée
Comparaison de la stratégie face au marché (Buy & Hold) :
![Performance Cumulée](Graphique%20Performance%20Cululée.png)

## Installation et Utilisation
1. Installer les dépendances : `pip install -r requirements.txt`
2. Lancer le script : `python backtest_sma.py`

## Métriques calculées
Le script génère automatiquement :
- CAGR (Taux de croissance annuel composé)
- Volatilité annualisée
- Ratio de Sharpe
- Max Drawdown
