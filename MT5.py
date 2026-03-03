import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import MetaTrader5 as mt5
from datetime import datetime, timedelta

# ==========================================
# 1. SETUP UI & CSS (FINAL NEAT DESIGN)
# ==========================================
st.set_page_config(page_title="AI Master Bot Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    /* Gaya Unified Metric Boxes */
    .metric-box {
        background-color: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #3e4251;
        border-left: 5px solid #58a6ff;
        text-align: center;
        height: 150px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .metric-title { color: #8b949e; font-size: 1rem; margin-bottom: 8px; }
    .metric-value { color: #ffffff; font-size: 1.8rem; font-weight: bold; }
    .pnl-pos { color: #00ff00; font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 10px #00ff00; }
    .pnl-neg { color: #ff0000; font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 10px #ff0000; }
    
    .disclaimer-card { background-color: #2b1111; padding: 20px; border-radius: 10px; border: 1px solid #ff4b4b; color: #ff8888; margin-bottom:15px; }
    .guide-card { background-color: #1e2130; padding: 20px; border-radius: 15px; border: 1px solid #3e4251; }
    
    div.stButton > button:first-child[kind="primary"] { background-color: #00ff00; color: black; font-weight: bold; box-shadow: 0 0 15px #00ff00; width: 100%; }
    div.stButton > button:first-child[kind="secondary"] { background-color: #ff0000; color: white; font-weight: bold; box-shadow: 0 0 15px #ff0000; width: 100%; }
    .status-online { color: #00ff00; font-weight: bold; font-size: 1.5rem; text-shadow: 0 0 10px #00ff00; margin-bottom: 10px; }
    .status-offline { color: #ff0000; font-weight: bold; font-size: 1.5rem; text-shadow: 0 0 10px #ff0000; margin-bottom: 10px; }
    
    .fx-box { border: 2px solid #58a6ff; padding:10px; border-radius:10px; margin-bottom: 5px; text-align: center; }
    .crypto-box { border: 2px solid #ff9500; padding:10px; border-radius:10px; margin-bottom: 5px; text-align: center; }
    .metal-box { border: 2px solid #ffcc00; padding:10px; border-radius:10px; margin-bottom: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE & DEFAULTS
# ==========================================
if 'connected' not in st.session_state: st.session_state.connected = False
if 'is_running' not in st.session_state: st.session_state.is_running = False
if 'logs' not in st.session_state: st.session_state.logs = []
if 'strategy_mode' not in st.session_state: st.session_state.strategy_mode = "COUNTER" 
if 'session_start_time' not in st.session_state: st.session_state.session_start_time = datetime.now()

defaults = {
    'set_lot': 0.01, 'set_sl_fx': 200, 'set_tp_fx': 400,
    'set_sl_crypto': 5000, 'set_tp_crypto': 10000,
    'set_sl_metal': 500, 'set_tp_metal': 1000,
    'run_categories': ["Forex", "Crypto", "Metal"],
    'strat_choice': 'Owner Default',
    'max_margin_pct': 60, 'max_symbols': 10
}
for key, val in defaults.items():
    if key not in st.session_state: st.session_state[key] = val

MAGIC_NUMBER = 777111
CRYPTO_LIST = ["BTC","ETH","SOL","XRP","DOGE","POL","AAVE","BCH","TRX","BNB","LTC","ADA"]
METAL_LIST = ["XAU","XAG","GOLD","SILVER","PLATINUM"]

def add_log(msg, log_type="info"):
    time_now = datetime.now().strftime("%H:%M:%S")
    emoji = "🔵" if log_type=="info" else "🟢" if log_type=="success" else "🔴"
    st.session_state.logs.insert(0, f"{emoji} [{time_now}] {msg}")

# ==========================================
# 3. INDICATOR ENGINE
# ==========================================
def EMA(data, n): return data.ewm(span=n, adjust=False).mean()
def RSI(data, n=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=n).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=n).mean()
    return 100 - (100 / (1 + (gain / loss.replace(0, np.nan))))

def detect_news(df):
    avg = abs(df['close'] - df['close'].shift(1)).rolling(10).mean().iloc[-1]
    return True if abs(df['close'].iloc[-1] - df['close'].iloc[-2]) > (avg * 2) else False

# ==========================================
# 4. STRATEGY ENGINE (10 STRATEGIES)
# ==========================================
def get_ai_signal(symbol, timeframe, strategy):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 250)
    if rates is None or len(rates) < 150: return "NONE"
    df = pd.DataFrame(rates)
    c = df['close']
    if any(x in symbol.upper() for x in METAL_LIST) and not detect_news(df): return "NONE"

    if strategy == "Owner Default": return "UP" if c.iloc[-1] > EMA(c, 5).iloc[-1] else "DOWN"
    elif strategy == "RSI Sniper":
        r = RSI(c, 14).iloc[-1]
        return "UP" if r < 30 else "DOWN" if r > 70 else "NONE"
    elif strategy == "Bollinger Reversion":
        ma, std = c.rolling(20).mean(), c.rolling(20).std()
        if c.iloc[-1] < (ma - std*2).iloc[-1]: return "UP"
        if c.iloc[-1] > (ma + std*2).iloc[-1]: return "DOWN"
    elif strategy == "MACD Zero-Cross":
        macd = EMA(c, 12) - EMA(c, 26)
        if macd.iloc[-1] > 0 and macd.iloc[-2] <= 0: return "UP"
        if macd.iloc[-1] < 0 and macd.iloc[-2] >= 0: return "DOWN"
    elif strategy == "Triple EMA Alignment":
        e9, e21, e50 = EMA(c, 9), EMA(c, 21), EMA(c, 50)
        if e9.iloc[-1] > e21.iloc[-1] > e50.iloc[-1]: return "UP"
        if e9.iloc[-1] < e21.iloc[-1] < e50.iloc[-1]: return "DOWN"
    elif strategy == "Stochastic Scalper":
        low14, high14 = df['low'].rolling(14).min(), df['high'].rolling(14).max()
        k = 100 * (c - low14) / (high14 - low14).replace(0, np.nan)
        return "UP" if k.iloc[-1] < 20 else "DOWN" if k.iloc[-1] > 80 else "NONE"
    elif strategy == "Price Breakout":
        h10, l10 = df['high'].shift(1).rolling(10).max().iloc[-1], df['low'].shift(1).rolling(10).min().iloc[-1]
        if c.iloc[-1] > h10: return "UP"
        if c.iloc[-1] < l10: return "DOWN"
    elif strategy == "Golden Cross":
        return "UP" if EMA(c, 50).iloc[-1] > EMA(c, 200).iloc[-1] else "DOWN"
    elif strategy == "Engulfing Tracker":
        if c.iloc[-1] > df['open'].iloc[-1] and df['open'].iloc[-1] > c.iloc[-2]: return "UP"
        if c.iloc[-1] < df['open'].iloc[-1] and df['open'].iloc[-1] < c.iloc[-2]: return "DOWN"
    elif strategy == "ATR Volatility":
        tr = pd.concat([df['high']-df['low'], abs(df['high']-c.shift(1)), abs(df['low']-c.shift(1))], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
        if (c.iloc[-1] - df['open'].iloc[-1]) > atr: return "UP"
        if (df['open'].iloc[-1] - c.iloc[-1]) > atr: return "DOWN"
    return "NONE"

# ==========================================
# 5. RISK & CORE FUNCTIONS
# ==========================================
def get_filling_mode(symbol):
    info = mt5.symbol_info(symbol)
    if info.filling_mode & 1: return mt5.ORDER_FILLING_FOK
    elif info.filling_mode & 2: return mt5.ORDER_FILLING_IOC
    else: return mt5.ORDER_FILLING_RETURN

def check_history_and_flip():
    deals = mt5.history_deals_get(datetime.now() - timedelta(days=1), datetime.now())
    if deals:
        bot_d = [d for d in deals if d.magic == MAGIC_NUMBER and d.profit != 0]
        bot_d.sort(key=lambda x: x.time, reverse=True)
        if len(bot_d) >= 2:
            if (bot_d[0].profit < 0 and bot_d[1].profit < 0) or (bot_d[0].profit > 0 and bot_d[1].profit > 0):
                st.session_state.strategy_mode = "FOLLOW" if st.session_state.strategy_mode == "COUNTER" else "COUNTER"

# ==========================================
# 6. SIDEBAR (PERSISTENT SETTINGS)
# ==========================================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/steam899/Web-design/refs/heads/main/Photoroom-20260303_123523421.png", use_container_width=True)
    if st.button("🔌 HUBUNGKAN MT5", use_container_width=True):
        if mt5.initialize(): st.session_state.connected = True

    if st.session_state.connected:
        st.markdown("---")
        up_file = st.file_uploader("📂 Upload Setting (.json)", type="json")
        if up_file:
            data = json.load(up_file)
            for k,v in data.items(): st.session_state[k] = v
            st.rerun()

        with st.expander("🎯 STRATEGI & ASSET", expanded=True):
            strat_list = ["Owner Default", "RSI Sniper", "Bollinger Reversion", "MACD Zero-Cross", "Triple EMA Alignment", "Stochastic Scalper", "Price Breakout", "Golden Cross", "Engulfing Tracker", "ATR Volatility"]
            st.session_state.strat_choice = st.selectbox("Strategi:", strat_list, index=strat_list.index(st.session_state.strat_choice))
            st.session_state.run_categories = st.multiselect("Asset:", ["Forex", "Crypto", "Metal"], default=st.session_state.run_categories)

        st.session_state.set_lot = st.number_input("Lot Size", 0.01, 10.0, value=st.session_state.set_lot)
        with st.expander("🌍 SL & TP SETTINGS"):
            st.session_state.set_sl_fx = st.number_input("FX SL", 10, 5000, value=st.session_state.set_sl_fx)
            st.session_state.set_tp_fx = st.number_input("FX TP", 10, 10000, value=st.session_state.set_tp_fx)
            st.session_state.set_sl_crypto = st.number_input("Crypto SL", 10, 100000, value=st.session_state.set_sl_crypto)
            st.session_state.set_tp_crypto = st.number_input("Crypto TP", 10, 100000, value=st.session_state.set_tp_crypto)
            st.session_state.set_sl_metal = st.number_input("Metal SL", 10, 100000, value=st.session_state.set_sl_metal)
            st.session_state.set_tp_metal = st.number_input("Metal TP", 10, 100000, value=st.session_state.set_tp_metal)
        
        st.session_state.max_margin_pct = st.slider("Had Margin (%)", 10, 100, value=st.session_state.max_margin_pct)
        st.session_state.max_symbols = st.slider("Scan Symbols", 1, 30, value=st.session_state.max_symbols)

        save_data = {k: st.session_state[k] for k in defaults.keys()}
        st.download_button("💾 Save Setting", json.dumps(save_data, indent=4), "ai_config.json", use_container_width=True)
        
        if st.button("▶️ MULA BOT", type="primary", use_container_width=True):
            st.session_state.session_start_time = datetime.now()
            st.session_state.is_running = True
        if st.button("⏹️ BERHENTI", type="secondary", use_container_width=True): st.session_state.is_running = False

# ==========================================
# 7. DASHBOARD UTAMA
# ==========================================
if st.session_state.connected:
    acc = mt5.account_info()
    st.markdown(f"<div style='text-align:center;' class='{'status-online' if st.session_state.is_running else 'status-offline'}'>BOT STATUS: {'ONLINE' if st.session_state.is_running else 'OFFLINE'}</div>", unsafe_allow_html=True)
    st.markdown(f"### 👤 {acc.name} | {acc.server}")
    
    # --- P&L CALCULATION (CLOSED ONLY) ---
    deals = mt5.history_deals_get(st.session_state.session_start_time, datetime.now())
    real_pnl = 0.0
    if deals:
        for d in [x for x in deals if x.magic == MAGIC_NUMBER and x.profit != 0]:
            real_pnl += (d.profit + d.swap + d.commission - (d.volume * 5.0))

    # Unified Glowing Boxes
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f"<div class='metric-box'><div class='metric-title'>Balance</div><div class='metric-value'>${acc.balance:,.2f}</div></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='metric-box'><div class='metric-title'>Equity</div><div class='metric-value'>${acc.equity:,.2f}</div></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='metric-box'><div class='metric-title'>Floating P&L</div><div class='{'pnl-pos' if acc.profit >= 0 else 'pnl-neg'}'>${acc.profit:,.2f}</div></div>", unsafe_allow_html=True)
    with col4: st.markdown(f"<div class='metric-box'><div class='metric-title'>P&L / Session</div><div class='{'pnl-pos' if real_pnl >= 0 else 'pnl-neg'}'>${real_pnl:,.2f}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    if not st.session_state.is_running:
        st.markdown("""
            <div class="disclaimer-card">
                <h4 style="margin:0;">⛔ PENAFIAN & AMARAN KERAS</h4>
                <p style="font-size:0.9rem;">1. Bot ini adalah harta intelek peribadi. <b>TIDAK BOLEH DIJUAL ATAU DIBELI</b>.<br>
                2. Dagangan Forex, Crypto, dan Metal melibatkan risiko kerugian modal yang tinggi.</p>
            </div>
            <div class="guide-card">
                <h4 style="color: #58a6ff;">🚀 PANDUAN ARAHAN</h4>
                <p style="font-size:0.95rem;">- Pastikan <b>Algo Trading</b> di MT5 berwarna Hijau.<br>- Drag simbol ke <b>Market Watch</b>.<br>- Klik <b>MULA BOT</b> untuk trade mengikut trend.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        check_history_and_flip()
        visible = [s for s in mt5.symbols_get() if s.visible][:st.session_state.max_symbols]
        can_trade = acc.margin < (acc.balance * (st.session_state.max_margin_pct / 100))
        
        for sym in visible:
            s_name = sym.name.upper()
            is_met = any(x in s_name for x in METAL_LIST)
            is_cry = any(x in s_name for x in CRYPTO_LIST)
            is_fx = not (is_met or is_cry)
            if (is_fx and "Forex" not in st.session_state.run_categories) or (is_cry and "Crypto" not in st.session_state.run_categories) or (is_met and "Metal" not in st.session_state.run_categories): continue

            # Timeframes: FX=H1, Crypto=W1, Metal=D1
            tf = mt5.TIMEFRAME_H1 if is_fx else mt5.TIMEFRAME_W1 if is_cry else mt5.TIMEFRAME_D1
            trend = get_ai_signal(s_name, tf, st.session_state.strat_choice)
            if trend == "NONE": continue
            
            sig = "BUY" if (st.session_state.strategy_mode == "COUNTER" and trend == "DOWN") or (st.session_state.strategy_mode == "FOLLOW" and trend == "UP") else "SELL" if (st.session_state.strategy_mode == "COUNTER" and trend == "UP") or (st.session_state.strategy_mode == "FOLLOW" and trend == "DOWN") else "WAIT"
            
            if sig != "WAIT" and can_trade and not mt5.positions_get(symbol=s_name):
                u_sl, u_tp = (st.session_state.set_sl_metal, st.session_state.set_tp_metal) if is_met else (st.session_state.set_sl_crypto, st.session_state.set_tp_crypto) if is_cry else (st.session_state.set_sl_fx, st.session_state.set_tp_fx)
                t = mt5.symbol_info_tick(s_name)
                if t:
                    p = t.ask if sig == "BUY" else t.bid
                    mt5.order_send({"action": mt5.TRADE_ACTION_DEAL, "symbol": s_name, "volume": float(st.session_state.set_lot), "type": mt5.ORDER_TYPE_BUY if sig == "BUY" else mt5.ORDER_TYPE_SELL, "price": p, "sl": p-(u_sl*sym.point) if sig=="BUY" else p+(u_sl*sym.point), "tp": p+(u_tp*sym.point) if sig=="BUY" else p-(u_tp*sym.point), "magic": MAGIC_NUMBER, "comment": "AI-FINAL", "type_time": mt5.ORDER_TIME_GTC, "type_filling": get_filling_mode(s_name)})

        # --- TABLES (3 CATEGORIES) ---
        t1, t2, t3 = st.tabs(["📂 Posisi Terbuka", "📜 Sejarah Closed", "📝 Log Aktiviti"])
        with t1:
            all_pos = mt5.positions_get()
            if all_pos:
                df_p = pd.DataFrame([p._asdict() for p in all_pos])
                c_fx, c_cry, c_met = st.columns(3)
                with c_fx:
                    st.markdown("<div class='fx-box'>🌍 Forex</div>", unsafe_allow_html=True)
                    st.dataframe(df_p[~df_p['symbol'].str.contains("|".join(CRYPTO_LIST+METAL_LIST), case=False)][['symbol','type','profit']], use_container_width=True)
                with c_cry:
                    st.markdown("<div class='crypto-box'>₿ Crypto</div>", unsafe_allow_html=True)
                    st.dataframe(df_p[df_p['symbol'].str.contains("|".join(CRYPTO_LIST), case=False)][['symbol','type','profit']], use_container_width=True)
                with c_met:
                    st.markdown("<div class='metal-box'>🛡️ Metal</div>", unsafe_allow_html=True)
                    st.dataframe(df_p[df_p['symbol'].str.contains("|".join(METAL_LIST), case=False)][['symbol','type','profit']], use_container_width=True)
            else: st.info("Tiada posisi aktif.")
        with t2:
            if deals:
                df_h = pd.DataFrame([d._asdict() for d in deals if d.magic == MAGIC_NUMBER and d.profit != 0])
                if not df_h.empty:
                    df_h['time'] = pd.to_datetime(df_h['time'], unit='s')
                    st.dataframe(df_h[['time','symbol','type','volume','profit']], use_container_width=True)
        with t3: st.dataframe(pd.DataFrame(st.session_state.logs, columns=["Aktiviti"]), use_container_width=True)
        
        time.sleep(2)
        st.rerun()
else:
    st.image("https://raw.githubusercontent.com/steam899/Web-design/refs/heads/main/Photoroom-20260303_123523421.png", width=300)
    st.info("💡 Sila klik 'HUBUNGKAN MT5'.")