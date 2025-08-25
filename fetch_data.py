import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# ===== CONFIG =====
TICKER = "^NSEI"  # Change this to any NSE stock, e.g., "RELIANCE.NS"
START_DATE = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
END_DATE = datetime.today().strftime('%Y-%m-%d')
SAVE_PATH = f"D:\Predictive analysis stock market\stock_data\{TICKER.replace('^', '').replace('.', '_')}_raw.csv"

# ===== DATA FETCH FUNCTION =====
def get_stock_data(ticker, start, end, save_path=None):
    print(f"Fetching data for {ticker} from {start} to {end}...")
    df = yf.download(ticker, start=start, end=end, interval='1d', group_by="column")

    # Flatten multi-index if it exists
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # If Adj Close missing, use Close
    if 'Adj Close' not in df.columns:
        df['Adj Close'] = df['Close']

    df.reset_index(inplace=True)
    df.sort_values("Date", inplace=True)

    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Data saved to {save_path}")

    return df


# ===== RUN =====
if __name__ == "__main__":
    df = get_stock_data(TICKER, START_DATE, END_DATE, SAVE_PATH)
    print(df.head())
