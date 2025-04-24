import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from data.data_fetcher import CryptoDataFetcher

def test_data_fetcher():
    print("Testing CryptoDataFetcher module...")
    
    # Initialize data fetcher
    data_fetcher = CryptoDataFetcher()
    print("✓ CryptoDataFetcher initialized successfully")
    
    # Test connecting to exchange
    print("\nTesting exchange connection...")
    success = data_fetcher.connect_exchange('Binance')
    if success:
        print("✓ Successfully connected to Binance")
    else:
        print("✗ Failed to connect to Binance")
    
    # Test sample data generation (this should work regardless of API access)
    print("\nTesting sample data generation...")
    sample_data = data_fetcher.generate_sample_data(symbol='BTC/USDT', days=5)
    if not sample_data.empty:
        print(f"✓ Successfully generated sample data with {len(sample_data)} rows")
        print("\nSample data preview:")
        print(sample_data.head())
    else:
        print("✗ Failed to generate sample data")
    
    # Test available exchanges
    print("\nAvailable exchanges:")
    for exchange in data_fetcher.available_exchanges.keys():
        print(f"- {exchange}")
    
    print("\nData fetcher test completed")

if __name__ == "__main__":
    test_data_fetcher()
