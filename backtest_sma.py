# -*- coding: utf-8 -*-
"""

#Auteur : Timeo Lemaitre
#Description :
    #Backtest complet d'une stratégie de croisement de moyennes mobiles
    #avec métriques professionnelles, gestion des coûts et visualisations.
"""


# 1. Importations

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# 2. Paramètres

TICKER = "AAPL"
START_DATE = "2020-01-01"
END_DATE = "2023-12-31"

SHORT_WINDOW = 20
LONG_WINDOW = 50

TRANSACTION_COST = 0.0005   # 5 bps
INITIAL_CAPITAL = 1.0



# 3. Fonctions utilitaires


def compute_cagr(series):
    #"""Calcule le CAGR (taux de croissance annuel composé)."""
    years = (series.index[-1] - series.index[0]).days / 365.25
    return (series.iloc[-1] / series.iloc[0])**(1 / years) - 1


def compute_volatility(returns):
    #"""Volatilité annualisée."""
    return returns.std() * np.sqrt(252)


def compute_sharpe(returns):
    #"""Sharpe ratio annualisé (sans taux sans risque)."""
    return returns.mean() / returns.std() * np.sqrt(252)


def compute_max_drawdown(series):
    """Drawdown maximal."""
    rolling_max = series.cummax()
    drawdown = series / rolling_max - 1
    return drawdown.min()



# 4. Téléchargement des données


data = yf.download(TICKER, start=START_DATE, end=END_DATE)
data = data[['Close']].copy()



# 5. Indicateurs techniques

data['SMA_short'] = data['Close'].rolling(SHORT_WINDOW).mean()
data['SMA_long'] = data['Close'].rolling(LONG_WINDOW).mean()

# 6. Signaux de trading


data['Signal'] = 0
data.loc[data['SMA_short'] > data['SMA_long'], 'Signal'] = 1
data.loc[data['SMA_short'] < data['SMA_long'], 'Signal'] = -1

# Position exécutée le jour suivant
data['Position'] = data['Signal'].shift(1).fillna(0)

# Détection des trades (changements de position)
data['Trade'] = data['Position'].diff().abs()


# 7. Backtest

data['Daily_Return'] = data['Close'].pct_change()
data['Strategy_Return'] = data['Daily_Return'] * data['Position']

# Coûts de transaction
data['Strategy_Return'] -= data['Trade'] * TRANSACTION_COST

# Capital cumulé
data['Cumulative_Market'] = (1 + data['Daily_Return']).cumprod() * INITIAL_CAPITAL
data['Cumulative_Strategy'] = (1 + data['Strategy_Return']).cumprod() * INITIAL_CAPITAL

# 8. Métriques de performance

cagr = compute_cagr(data['Cumulative_Strategy'])
vol = compute_volatility(data['Strategy_Return'])
sharpe = compute_sharpe(data['Strategy_Return'])
max_dd = compute_max_drawdown(data['Cumulative_Strategy'])


# 9. Visualisations


# Graphique prix + SMA
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Prix')
plt.plot(data['SMA_short'], label=f'SMA {SHORT_WINDOW}')
plt.plot(data['SMA_long'], label=f'SMA {LONG_WINDOW}')

# Points d'entrée/sortie
buy_signals = data[data['Position'].diff() == 2]
sell_signals = data[data['Position'].diff() == -2]

plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', s=100, label='Achat')
plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='r', s=100, label='Vente')

plt.title(f"Stratégie SMA sur {TICKER}")
plt.xlabel("Date")
plt.ylabel("Prix")
plt.legend()
plt.grid(True)
plt.show()

# Graphique performance cumulée
plt.figure(figsize=(14, 7))
plt.plot(data['Cumulative_Market'], label='Marché')
plt.plot(data['Cumulative_Strategy'], label='Stratégie')
plt.title("Performance cumulée")
plt.xlabel("Date")
plt.ylabel("Capital relatif")
plt.legend()
plt.grid(True)
plt.show()

# 10. Résultats + Export

print("\n===== Résultats du Backtest =====")
print(f"CAGR : {cagr:.2%}")
print(f"Volatilité annualisée : {vol:.2%}")
print(f"Sharpe ratio : {sharpe:.2f}")
print(f"Max Drawdown : {max_dd:.2%}")

data.to_csv(f"{TICKER}_backtest_SMA.csv")
print(f"\nFichier exporté : {TICKER}_backtest_SMA.csv")
