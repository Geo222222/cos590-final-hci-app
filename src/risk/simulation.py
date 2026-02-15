import numpy as np
import pandas as pd
import os

def get_market_data(n_assets: int, n_periods: int, seed: int = 7):
    """
    Loads real ETH/USDT data from CSV.
    If n_assets > 1, generates synthetic correlated assets based on ETH returns
    to simulate a crypto portfolio.
    """
    # Go up 4 levels to get to project root: src/risk/simulation.py -> src/risk -> src -> hci_app -> project_root
    # Path to the data file within the package (hci_app/data/eth_usdt_1h.csv)
    # src/risk/simulation.py -> src/risk -> src -> hci_app
    app_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(app_root, "data/eth_usdt_1h.csv")
    
    if not os.path.exists(csv_path):
        # Fallback to pure synthetic if file missing
        print(f"Warning: Data file not found at {csv_path}. Using random generation.")
        rng = np.random.default_rng(seed)
        mus = rng.normal(0.0003, 0.0002, size=n_assets)
        sigmas = rng.uniform(0.005, 0.03, size=n_assets)
        dates = pd.date_range(end=pd.Timestamp.now(), periods=n_periods, freq='H')
        return rng.normal(mus, sigmas, size=(n_periods, n_assets)), dates

    # Read CSV
    # yfinance to_csv produces a 3-row header structure effectively
    # Row 0: Ticker
    # Row 1: Price
    # Row 2: Metadata (sometimes)
    # We'll read carefully.
    try:
        df = pd.read_csv(csv_path, header=[0, 1], index_col=0, parse_dates=True)
        
        # Depending on pandas version and read_csv, the header handling might vary.
        # We look for 'Close' in the second level.
        close_col = None
        for col in df.columns:
            if col[1] == 'Close':
                close_col = col
                break
        
        if close_col is None:
            # Try single level if formatting is different
            if 'Close' in df.columns:
                prices = df['Close']
            else:
                raise ValueError("Close column not found")
        else:
            prices = df[close_col]
            
        # Clean data
        prices = prices.ffill().bfill()
        returns = prices.pct_change().dropna()
        
        # Slice to requested periods (take most recent)
        # Note: dataset is ~6 months (~4300 hours)
        if len(returns) > n_periods:
            returns = returns.iloc[-n_periods:]
        elif len(returns) < n_periods:
            # If we don't have enough data, we MUST return what we have
            # rather than failing or padding poorly.
            pass 
            
        base_rets = returns.values.flatten()
        
        # Handle n_assets
        if n_assets == 1:
            return base_rets.reshape(-1, 1), returns.index
            
        # Generate correlated assets
        rng = np.random.default_rng(seed)
        assets_rets = np.zeros((len(base_rets), n_assets))
        assets_rets[:, 0] = base_rets
        
        vol = np.std(base_rets)
        for i in range(1, n_assets):
            # Create variations: some correlated, some noisier
            # Noise level: 0.5 * volatility
            noise = rng.normal(0, vol * 0.8, size=len(base_rets))
            # Maybe some slight drift diff
            drift_adj = rng.normal(0, 0.0001)
            assets_rets[:, i] = base_rets + noise + drift_adj
            
        return assets_rets, returns.index
        
    except Exception as e:
        print(f"Error reading market data: {e}")
        # Fallback
        rng = np.random.default_rng(seed)
        # Generate dummy dates for fallback
        dates = pd.date_range(end=pd.Timestamp.now(), periods=n_periods, freq='H')
        return rng.normal(0.0003, 0.01, size=(n_periods, n_assets)), dates

def get_full_market_data():
    app_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(app_root, "data/eth_usdt_1h.csv")
    df = pd.read_csv(csv_path, header=[0, 1], index_col=0, parse_dates=True)
    df.columns = df.columns.droplevel(0)
    df.reset_index(inplace=True)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    return df

