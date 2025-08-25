import pandas as pd
import ta

# ===== PREPROCESSING FUNCTION =====
def preprocess_data(df):
    # Ensure date is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Remove missing rows
    df.dropna(inplace=True)

    # Technical Indicators
    df['SMA_10'] = ta.trend.sma_indicator(df['Adj Close'], window=10)
    df['SMA_50'] = ta.trend.sma_indicator(df['Adj Close'], window=50)
    df['EMA_10'] = ta.trend.ema_indicator(df['Adj Close'], window=10)
    df['RSI_14'] = ta.momentum.rsi(df['Adj Close'], window=14)
    df['MACD'] = ta.trend.macd_diff(df['Adj Close'])
    
    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['Adj Close'], window=20, window_dev=2)
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()

    # Daily Returns
    df['Daily_Return'] = df['Adj Close'].pct_change()

    # Lag Features
    df['Lag_1'] = df['Adj Close'].shift(1)
    df['Lag_2'] = df['Adj Close'].shift(2)
    df['Lag_3'] = df['Adj Close'].shift(3)

    # Target Variable: 1 if next day's close > today's close, else 0
    df['Target'] = (df['Adj Close'].shift(-1) > df['Adj Close']).astype(int)

    # Drop rows with NaNs from indicator calculations
    df.dropna(inplace=True)

    return df

# ===== RUN =====
if __name__ == "__main__":
    from fetch_data import get_stock_data  
    df = get_stock_data("^NSEI", "2018-06-10", "2025-06-10")
    processed_df = preprocess_data(df)
    processed_df.to_csv("stock_data/NSEI_processed.csv", index=False)
    print(processed_df.head())
