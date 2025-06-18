import talib
import numpy as np

def analyze_market(client):
    candles = client.get_candles()
    closes = np.array([c['close'] for c in candles])
    
    # Calculate indicators
    rsi = talib.RSI(closes, timeperiod=3)
    ema9 = talib.EMA(closes, timeperiod=9)
    
    # Strategy logic
    current_price = closes[-1]
    
    # S/R Bounce Strategy
    if rsi[-1] < 30 and current_price <= ema9[-1]:
        return {
            "direction": "BUY",
            "pair": client.current_pair,
            "entry": current_price,
            "tp": current_price * 1.0010,  # 0.1% TP
            "sl": current_price * 0.9995    # 0.05% SL
        }
    
    # Add more strategies...
    
    return None