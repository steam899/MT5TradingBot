# AI Master Bot Pro

**AI Master Bot Pro** is a trading bot built with **MetaTrader 5 (MT5)**, designed for automated trading using AI-powered strategies in Forex, Crypto, and Metal markets. This bot leverages technical indicators like **EMA**, **RSI**, and **MACD** to analyze market trends and make real-time buy/sell decisions.

## Features

- **AI-based Trading Strategies**:  
  The bot supports multiple trading strategies such as:
  - Owner Default
  - RSI Sniper
  - Bollinger Reversion
  - MACD Zero-Cross
  - Triple EMA Alignment
  - Stochastic Scalper
  - Price Breakout
  - Golden Cross
  - Engulfing Tracker
  - ATR Volatility
  
- **Real-Time Position Management**:  
  Track open positions, profit/loss, and historical trades.

- **Risk Management**:  
  Set Stop-Loss (SL) and Take-Profit (TP) levels for different asset classes:
  - Forex
  - Crypto
  - Metals
  
- **Dynamic Strategy Switching**:  
  The bot can automatically switch between **COUNTER** and **FOLLOW** strategy modes based on historical performance (wins/losses).

- **Customizable Settings**:  
  Configure trading strategies, risk parameters (SL, TP, margin), and asset categories directly from the Streamlit UI.

## Requirements

- **MetaTrader 5 (MT5)**: You must have a MetaTrader 5 account and trading platform configured.
- **Python 3.x**: The bot is built using Python and requires Python 3.x.
- **Libraries**: The following Python libraries are required to run this bot:
  - `streamlit`
  - `pandas`
  - `numpy`
  - `MetaTrader5`
  - `json`
  
  Install the required libraries with:
  ```bash
  pip install streamlit pandas numpy MetaTrader5


1. Clone the Repository

Clone the repository to your local machine:

git clone https://github.com/yourusername/ai-master-bot-pro.git
cd ai-master-bot-pro

2. Install Dependencies

Ensure you have the necessary Python libraries installed:

pip install -r requirements.txt

3. Run the Streamlit App

Start the Streamlit application to open the bot’s interface:

streamlit run app.py

The app will open in your browser, and you can start configuring and running your AI trading bot.

4. Connect to MT5

Click on the "🔌 HUBUNGKAN MT5" button to connect the bot to your MT5 account. Ensure that your MetaTrader 5 account is properly configured and connected to the platform.

5. Configure Settings

Upload your .json settings file or configure your bot directly through the UI.

Select the trading strategy and asset categories you wish to use (Forex, Crypto, Metal).

Set your Stop-Loss and Take-Profit values for each asset class.

Adjust your Lot Size and Margin settings.

6. Start the Bot

Click on "▶️ MULA BOT" to start the bot and begin trading. The bot will automatically make trades based on the selected strategy and current market trends.

7. Monitor & Manage Positions

View open positions and monitor your profit/loss.

Review historical trades and activity logs.

The bot will display real-time updates on account balance, equity, and P&L.

8. Stop the Bot

Click on "⏹️ BERHENTI" to stop the bot.

Settings File Format

You can upload a .json file to customize the bot’s settings. Here's an example of the settings file:

{
    "set_lot": 0.01,
    "set_sl_fx": 200,
    "set_tp_fx": 400,
    "set_sl_crypto": 5000,
    "set_tp_crypto": 10000,
    "set_sl_metal": 500,
    "set_tp_metal": 1000,
    "run_categories": ["Forex", "Crypto", "Metal"],
    "strat_choice": "Owner Default",
    "max_margin_pct": 60,
    "max_symbols": 10
}
Customization

You can customize various parameters such as:

Lot Size (set_lot)

Stop Loss (SL) and Take Profit (TP) for Forex, Crypto, and Metal.

Risk Settings: Maximum margin percentage and maximum symbols to trade.

Strategy Mode: COUNTER or FOLLOW based on previous trades.

Troubleshooting

MT5 Not Connecting: Make sure your MT5 account is properly configured and that the MetaTrader 5 terminal is running.

Data Errors: Ensure your internet connection is stable. If the bot isn't receiving market data, try reconnecting MT5.

For more troubleshooting or questions, please open an issue in this repository.

Contributing

Contributions are welcome! Feel free to fork this project, open issues, and submit pull requests.

Fork the repository

Create your feature branch: git checkout -b feature-branch

Commit your changes: git commit -am 'Add new feature'

Push to the branch: git push origin feature-branch

Open a pull request

License

This project is licensed under the MIT License - see the LICENSE
 file for details.

