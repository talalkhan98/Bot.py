import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
from data.data_fetcher import CryptoDataFetcher
from analysis.indicators import TechnicalIndicators
from strategies.trading_strategies import TradingStrategies
from ui.components import UIComponents

def test_streamlit_components():
    print("Testing Streamlit UI components...")
    
    # Initialize components
    data_fetcher = CryptoDataFetcher()
    indicators = TechnicalIndicators()
    strategies = TradingStrategies()
    ui = UIComponents()
    
    print("✓ All components initialized successfully")
    
    # Generate sample data
    sample_data = data_fetcher.generate_sample_data(symbol='BTC/USDT', days=30)
    print(f"✓ Generated sample data with {len(sample_data)} rows")
    
    # Add indicators
    data_with_indicators = indicators.add_all_indicators(sample_data)
    print(f"✓ Added technical indicators to data")
    
    # Apply strategy
    strategy_result = strategies.apply_strategy(sample_data, "RSI Strategy")
    print(f"✓ Applied RSI strategy to data")
    
    # Backtest strategy
    backtest_df, metrics = strategies.backtest_strategy(strategy_result)
    print(f"✓ Backtested strategy successfully")
    
    # Generate market summary
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    market_data = []
    for symbol in symbols:
        market_data.append({
            'symbol': symbol,
            'last_price': np.random.uniform(10000, 60000) if 'BTC' in symbol else np.random.uniform(1000, 4000) if 'ETH' in symbol else np.random.uniform(50, 200),
            'daily_change': np.random.uniform(-5, 5),
            'volume_24h': np.random.uniform(1000000, 10000000),
            'high_24h': np.random.uniform(10000, 60000) if 'BTC' in symbol else np.random.uniform(1000, 4000) if 'ETH' in symbol else np.random.uniform(50, 200),
            'low_24h': np.random.uniform(10000, 60000) if 'BTC' in symbol else np.random.uniform(1000, 4000) if 'ETH' in symbol else np.random.uniform(50, 200)
        })
    market_summary = pd.DataFrame(market_data)
    print(f"✓ Generated market summary data")
    
    # Test UI component methods
    print("\nTesting UI component methods...")
    
    # Test format_number method
    test_numbers = [0.00000123, 0.123, 12.34, 1234, 1234567, 1234567890]
    for num in test_numbers:
        formatted = ui.format_number(num)
        print(f"✓ format_number({num}) = {formatted}")
    
    # Test render methods (these would normally render in Streamlit)
    print("\nChecking render methods (no actual rendering in test)...")
    methods = [
        "render_header", 
        "render_market_summary", 
        "render_price_chart",
        "render_indicator_charts",
        "render_rsi_chart",
        "render_macd_chart",
        "render_bollinger_bands_chart",
        "render_moving_averages_chart",
        "render_volume_chart",
        "render_stochastic_chart",
        "render_atr_chart",
        "render_backtest_results",
        "render_trade_signals",
        "render_strategy_optimizer",
        "render_live_trading_status"
    ]
    
    for method in methods:
        if hasattr(ui, method):
            print(f"✓ UI has method: {method}")
        else:
            print(f"✗ UI missing method: {method}")
    
    print("\nStreamlit UI components test completed")

if __name__ == "__main__":
    test_streamlit_components()
