# 🚀 AI Master Bot Pro

### Institutional-Grade Multi-Asset Trading System (MT5 + Streamlit)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-MetaTrader5-green)
![UI](https://img.shields.io/badge/UI-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

------------------------------------------------------------------------

## 🌟 Overview

**AI Master Bot Pro** is a professional-grade automated trading system
built for **MetaTrader 5 (MT5)** with a modern web-based dashboard
powered by Streamlit.

Designed for serious traders, this system supports **Forex, Crypto, and
Metals** with intelligent strategy switching, risk controls, and live
performance monitoring.

------------------------------------------------------------------------

## 🧠 Core Capabilities

### 🔹 Multi-Asset Trading

-   Forex (H1 timeframe)
-   Cryptocurrency (W1 timeframe)
-   Metals (D1 timeframe)

### 🔹 10 Built-In Trading Strategies

-   Owner Default (EMA-based trend logic)
-   RSI Sniper
-   Bollinger Reversion
-   MACD Zero-Cross
-   Triple EMA Alignment
-   Stochastic Scalper
-   Price Breakout
-   Golden Cross
-   Engulfing Tracker
-   ATR Volatility Expansion

### 🔹 Intelligent Strategy Mode

-   **FOLLOW Mode** → Trades with trend
-   **COUNTER Mode** → Trades against trend
-   Auto-switching after consecutive identical results (win/win or
    loss/loss)

------------------------------------------------------------------------

## 📊 Advanced Dashboard

✔ Live Account Balance & Equity\
✔ Floating P&L Monitoring\
✔ Session-Based Realized P&L\
✔ Categorized Open Positions\
✔ Closed Trade History\
✔ Activity Logs\
✔ Margin Usage Protection

Modern dark UI with institutional-style metric boxes and real-time
updates.

------------------------------------------------------------------------

## 🛡 Risk Management Engine

-   Custom Stop Loss & Take Profit per asset category
-   Adjustable Lot Size
-   Margin Usage Cap (% Protection)
-   Maximum Symbol Scanner Control
-   Magic Number Isolation (777111)

------------------------------------------------------------------------

## 🏗 System Architecture

Frontend: - Streamlit UI - Dynamic session state management - JSON
configuration persistence

Backend: - MetaTrader5 Python API - Pandas & NumPy indicator engine -
Automated order execution logic - Strategy signal engine (250-candle
analysis window)

------------------------------------------------------------------------

## ⚙ Installation

### 1. Clone Repository

``` bash
git clone https://github.com/steam899/MT5TradingBot.git
cd MT5TradingBot
```

### 2. Install Dependencies

``` bash
pip install streamlit pandas numpy MetaTrader5
```

------------------------------------------------------------------------

## ▶ How to Run

Make sure:

-   MetaTrader 5 is installed
-   You are logged into your trading account
-   Algo Trading is enabled (Green)

Run:

``` bash
streamlit run MT5.py
```

Open your browser at:

    http://localhost:8501

------------------------------------------------------------------------

## 🔧 Configuration Management

You can:

-   Upload custom JSON configuration files
-   Download current strategy settings
-   Persist trading preferences across sessions

------------------------------------------------------------------------

## 📈 Trading Logic Summary

-   Forex → H1 Trend Model
-   Crypto → Weekly Macro Bias
-   Metals → Daily Structural Momentum
-   Automatic news volatility detection (Metals filter)
-   Position filtering to prevent duplicate trades
-   Real-time symbol scanning (configurable limit)

------------------------------------------------------------------------

## ⚠ Risk Disclaimer

Trading Forex, Cryptocurrency, and Metals involves significant financial
risk and may not be suitable for all investors.

This software is provided for educational and research purposes only.\
Always test on a demo account before deploying to live capital.

The developer assumes no responsibility for financial losses.

------------------------------------------------------------------------

## 🔮 Roadmap

-   Telegram Trade Notifications
-   Performance Analytics Report Export
-   Backtesting Module
-   VPS Deployment Automation
-   Multi-Account Scaling

------------------------------------------------------------------------

## 👨‍💻 Author

AI Master Bot Pro\
Private Proprietary System\
© 2026 All Rights Reserved

------------------------------------------------------------------------

### 💎 Professional. Intelligent. Automated.
