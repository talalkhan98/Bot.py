import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from data.data_fetcher import CryptoDataFetcher
from analysis.indicators import TechnicalIndicators

def test_technical_indicators():
    print("Testing TechnicalIndicators module...")
    
    # Initialize data fetcher to get sample data
    data_fetcher = CryptoDataFetcher()
    sample_data = data_fetcher.generate_sample_data(symbol='BTC/USDT', days=30)
    print(f"✓ Generated sample data with {len(sample_data)} rows")
    
    # Initialize technical indicators
    indicators = TechnicalIndicators()
    print("✓ TechnicalIndicators initialized successfully")
    
    # Test adding moving averages
    print("\nTesting moving averages...")
    try:
        df_with_ma = indicators.add_moving_averages(sample_data)
        ma_columns = [col for col in df_with_ma.columns if 'sma_' in col or 'ema_' in col]
        print(f"✓ Added moving averages: {ma_columns}")
    except Exception as e:
        print(f"✗ Failed to add moving averages: {str(e)}")
    
    # Test adding RSI
    print("\nTesting RSI...")
    try:
        df_with_rsi = indicators.add_rsi(sample_data)
        if 'rsi_14' in df_with_rsi.columns:
            print(f"✓ Added RSI indicator")
            print(f"  RSI range: {df_with_rsi['rsi_14'].min():.2f} to {df_with_rsi['rsi_14'].max():.2f}")
        else:
            print("✗ RSI column not found in result")
    except Exception as e:
        print(f"✗ Failed to add RSI: {str(e)}")
    
    # Test adding MACD
    print("\nTesting MACD...")
    try:
        df_with_macd = indicators.add_macd(sample_data)
        macd_columns = [col for col in df_with_macd.columns if 'macd' in col]
        if macd_columns:
            print(f"✓ Added MACD indicators: {macd_columns}")
        else:
            print("✗ MACD columns not found in result")
    except Exception as e:
        print(f"✗ Failed to add MACD: {str(e)}")
    
    # Test adding Bollinger Bands
    print("\nTesting Bollinger Bands...")
    try:
        df_with_bb = indicators.add_bollinger_bands(sample_data)
        bb_columns = [col for col in df_with_bb.columns if 'bollinger' in col]
        if bb_columns:
            print(f"✓ Added Bollinger Bands indicators: {bb_columns}")
        else:
            print("✗ Bollinger Bands columns not found in result")
    except Exception as e:
        print(f"✗ Failed to add Bollinger Bands: {str(e)}")
    
    # Test adding all indicators
    print("\nTesting adding all indicators...")
    try:
        df_with_all = indicators.add_all_indicators(sample_data)
        indicator_count = len(df_with_all.columns) - len(sample_data.columns)
        print(f"✓ Added {indicator_count} technical indicators")
    except Exception as e:
        print(f"✗ Failed to add all indicators: {str(e)}")
    
    # Test signal identification
    print("\nTesting signal identification...")
    try:
        df_with_signals = indicators.identify_signals(df_with_all)
        signal_columns = [col for col in df_with_signals.columns if 'signal' in col]
        if signal_columns:
            print(f"✓ Identified trading signals: {signal_columns}")
        else:
            print("✗ Signal columns not found in result")
    except Exception as e:
        print(f"✗ Failed to identify signals: {str(e)}")
    
    # Test getting current signals
    print("\nTesting current signals...")
    try:
        current_signals = indicators.get_current_signals(df_with_signals)
        if current_signals:
            print(f"✓ Got current signals:")
            for key, value in current_signals.items():
                print(f"  - {key}: {value}")
        else:
            print("✗ No current signals returned")
    except Exception as e:
        print(f"✗ Failed to get current signals: {str(e)}")
    
    print("\nTechnical indicators test completed")

if __name__ == "__main__":
    test_technical_indicators()
