import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from data.data_fetcher import CryptoDataFetcher
from analysis.indicators import TechnicalIndicators
from strategies.trading_strategies import TradingStrategies

def test_trading_strategies():
    print("Testing TradingStrategies module...")
    
    # Initialize data fetcher to get sample data
    data_fetcher = CryptoDataFetcher()
    sample_data = data_fetcher.generate_sample_data(symbol='BTC/USDT', days=60)
    print(f"✓ Generated sample data with {len(sample_data)} rows")
    
    # Initialize trading strategies
    strategies = TradingStrategies()
    print("✓ TradingStrategies initialized successfully")
    
    # Test RSI strategy
    print("\nTesting RSI strategy...")
    try:
        rsi_result = strategies.rsi_strategy(sample_data)
        signal_count = len(rsi_result[rsi_result['signal'] != 0])
        print(f"✓ Applied RSI strategy, generated {signal_count} signals")
    except Exception as e:
        print(f"✗ Failed to apply RSI strategy: {str(e)}")
    
    # Test MACD strategy
    print("\nTesting MACD strategy...")
    try:
        macd_result = strategies.macd_strategy(sample_data)
        signal_count = len(macd_result[macd_result['signal'] != 0])
        print(f"✓ Applied MACD strategy, generated {signal_count} signals")
    except Exception as e:
        print(f"✗ Failed to apply MACD strategy: {str(e)}")
    
    # Test Bollinger Bands strategy
    print("\nTesting Bollinger Bands strategy...")
    try:
        bb_result = strategies.bollinger_bands_strategy(sample_data)
        signal_count = len(bb_result[bb_result['signal'] != 0])
        print(f"✓ Applied Bollinger Bands strategy, generated {signal_count} signals")
    except Exception as e:
        print(f"✗ Failed to apply Bollinger Bands strategy: {str(e)}")
    
    # Test Moving Average Crossover strategy
    print("\nTesting Moving Average Crossover strategy...")
    try:
        ma_result = strategies.ma_crossover_strategy(sample_data)
        signal_count = len(ma_result[ma_result['signal'] != 0])
        print(f"✓ Applied Moving Average Crossover strategy, generated {signal_count} signals")
    except Exception as e:
        print(f"✗ Failed to apply Moving Average Crossover strategy: {str(e)}")
    
    # Test Custom strategy
    print("\nTesting Custom strategy...")
    try:
        custom_result = strategies.custom_strategy(sample_data)
        signal_count = len(custom_result[custom_result['signal'] != 0])
        print(f"✓ Applied Custom strategy, generated {signal_count} signals")
    except Exception as e:
        print(f"✗ Failed to apply Custom strategy: {str(e)}")
    
    # Test apply_strategy function
    print("\nTesting apply_strategy function...")
    try:
        strategy_result = strategies.apply_strategy(sample_data, "RSI Strategy")
        signal_count = len(strategy_result[strategy_result['signal'] != 0])
        print(f"✓ Applied strategy through apply_strategy function, generated {signal_count} signals")
    except Exception as e:
        print(f"✗ Failed to apply strategy through apply_strategy function: {str(e)}")
    
    # Test backtesting
    print("\nTesting backtesting...")
    try:
        backtest_df, metrics = strategies.backtest_strategy(strategy_result)
        print(f"✓ Backtesting completed successfully")
        print("  Backtest metrics:")
        for key, value in metrics.items():
            print(f"  - {key}: {value}")
    except Exception as e:
        print(f"✗ Failed to backtest strategy: {str(e)}")
    
    # Test trade signals generation
    print("\nTesting trade signals generation...")
    try:
        trade_signals = strategies.generate_trade_signals(strategy_result)
        print(f"✓ Generated {len(trade_signals)} trade signals")
    except Exception as e:
        print(f"✗ Failed to generate trade signals: {str(e)}")
    
    # Test strategy optimization
    print("\nTesting strategy optimization (simplified test)...")
    try:
        param_grid = {'overbought': [70, 75], 'oversold': [25, 30]}
        best_params, best_metrics = strategies.optimize_strategy(
            sample_data.iloc[:100], "RSI Strategy", param_grid
        )
        print(f"✓ Strategy optimization completed successfully")
        print("  Best parameters:")
        for key, value in best_params.items():
            print(f"  - {key}: {value}")
        print("  Best metrics:")
        for key, value in best_metrics.items():
            if key in ['total_return', 'annual_return', 'sharpe_ratio', 'max_drawdown']:
                print(f"  - {key}: {value}")
    except Exception as e:
        print(f"✗ Failed to optimize strategy: {str(e)}")
    
    print("\nTrading strategies test completed")

if __name__ == "__main__":
    test_trading_strategies()
