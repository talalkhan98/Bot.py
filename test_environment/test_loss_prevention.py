import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from data.data_fetcher import CryptoDataFetcher
from analysis.indicators import TechnicalIndicators
from strategies.trading_strategies import TradingStrategies
from utils.loss_prevention import LossPreventionSystem

def test_loss_prevention():
    print("Testing Loss Prevention System...")
    
    # Initialize components
    data_fetcher = CryptoDataFetcher()
    indicators = TechnicalIndicators()
    strategies = TradingStrategies()
    loss_prevention = LossPreventionSystem()
    
    print("✓ All components initialized successfully")
    
    # Generate sample data
    sample_data = data_fetcher.generate_sample_data(symbol='BTC/USDT', days=30)
    print(f"✓ Generated sample data with {len(sample_data)} rows")
    
    # Add indicators
    data_with_indicators = indicators.add_all_indicators(sample_data)
    print(f"✓ Added technical indicators to data")
    
    # Test position size calculation
    print("\nTesting position size calculation...")
    account_balance = 10000
    entry_price = 50000
    stop_loss = 48000
    volatility = 0.5
    
    position_size = loss_prevention.calculate_position_size(
        account_balance=account_balance,
        entry_price=entry_price,
        stop_loss=stop_loss,
        volatility=volatility
    )
    
    print(f"✓ Calculated position size: {position_size:.6f} BTC (${position_size * entry_price:.2f})")
    print(f"  Risk per trade: ${account_balance * (loss_prevention.max_risk_per_trade_pct / 100):.2f}")
    print(f"  Max position size: ${account_balance * (loss_prevention.max_position_size_pct / 100):.2f}")
    
    # Test stop loss calculation
    print("\nTesting stop loss calculation...")
    atr = data_with_indicators['atr_14'].iloc[-1]
    
    # ATR-based stop loss
    atr_stop = loss_prevention.calculate_stop_loss(
        entry_price=entry_price,
        direction=1,  # Long
        atr=atr
    )
    
    # Fixed percentage stop loss
    fixed_stop = loss_prevention.calculate_stop_loss(
        entry_price=entry_price,
        direction=1,  # Long
        fixed_pct=3.0
    )
    
    print(f"✓ Calculated ATR-based stop loss: ${atr_stop:.2f} ({(entry_price - atr_stop) / entry_price * 100:.2f}% from entry)")
    print(f"✓ Calculated fixed percentage stop loss: ${fixed_stop:.2f} (3.00% from entry)")
    
    # Test take profit calculation
    print("\nTesting take profit calculation...")
    take_profit = loss_prevention.calculate_take_profit(
        entry_price=entry_price,
        stop_loss=fixed_stop,
        direction=1,  # Long
        risk_reward_ratio=2.0
    )
    
    print(f"✓ Calculated take profit: ${take_profit:.2f} ({(take_profit - entry_price) / entry_price * 100:.2f}% from entry)")
    print(f"  Risk-reward ratio: 2.0")
    
    # Test trailing stop update
    print("\nTesting trailing stop update...")
    current_price = 52000  # Price moved up
    updated_stop = loss_prevention.update_trailing_stop(
        entry_price=entry_price,
        current_price=current_price,
        current_stop=fixed_stop,
        direction=1  # Long
    )
    
    print(f"✓ Updated trailing stop: ${updated_stop:.2f} ({(current_price - updated_stop) / current_price * 100:.2f}% from current price)")
    print(f"  Original stop: ${fixed_stop:.2f}")
    print(f"  Trailing stop percentage: {loss_prevention.trailing_stop_pct:.1f}%")
    
    # Test market conditions assessment
    print("\nTesting market conditions assessment...")
    market_conditions = loss_prevention.check_market_conditions(data_with_indicators)
    
    print(f"✓ Market conditions assessment:")
    print(f"  Market regime: {market_conditions['market_regime']}")
    print(f"  Volatility: {market_conditions['volatility']:.4f}")
    print(f"  Trend strength: {market_conditions['trend_strength']:.2f}")
    print(f"  Risk factor: {market_conditions['risk_factor']:.2f}")
    
    # Test risk adjustment
    print("\nTesting risk adjustment for market conditions...")
    adjusted_params = loss_prevention.adjust_risk_for_market_conditions(market_conditions)
    
    print(f"✓ Adjusted risk parameters:")
    print(f"  Original max position size: {loss_prevention.max_position_size_pct:.2f}%")
    print(f"  Adjusted max position size: {adjusted_params['max_position_size_pct']:.2f}%")
    print(f"  Original max risk per trade: {loss_prevention.max_risk_per_trade_pct:.2f}%")
    print(f"  Adjusted max risk per trade: {adjusted_params['max_risk_per_trade_pct']:.2f}%")
    
    # Test correlation filtering
    print("\nTesting correlation filtering...")
    # Create sample correlation matrix
    assets = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT']
    corr_data = np.array([
        [1.0, 0.8, 0.6, 0.4, 0.3],
        [0.8, 1.0, 0.7, 0.5, 0.4],
        [0.6, 0.7, 1.0, 0.3, 0.2],
        [0.4, 0.5, 0.3, 1.0, 0.9],
        [0.3, 0.4, 0.2, 0.9, 1.0]
    ])
    corr_matrix = pd.DataFrame(corr_data, index=assets, columns=assets)
    
    correlated_pairs = loss_prevention.filter_correlated_assets(corr_matrix)
    
    print(f"✓ Identified highly correlated asset pairs:")
    for pair in correlated_pairs:
        print(f"  - {pair[0]} and {pair[1]}")
    
    # Test risk report generation
    print("\nTesting risk report generation...")
    # Create sample trade history
    trades = pd.DataFrame({
        'symbol': ['BTC/USDT'] * 10,
        'type': ['BUY', 'SELL'] * 5,
        'price': [50000, 51000, 49000, 50500, 48000, 49500, 52000, 53000, 51500, 52500],
        'size': [0.1] * 10,
        'profit_loss': [100, -50, 150, -80, 200, -30, 120, -60, 90, -40]
    })
    
    # Create sample open positions
    open_positions = [
        {'symbol': 'BTC/USDT', 'type': 'LONG', 'entry_price': 50000, 'size': 0.1, 'value': 5000},
        {'symbol': 'ETH/USDT', 'type': 'LONG', 'entry_price': 3000, 'size': 1.0, 'value': 3000}
    ]
    
    risk_report = loss_prevention.generate_risk_report(trades, account_balance, open_positions)
    
    print(f"✓ Generated risk report:")
    print(f"  Total exposure: ${risk_report['total_exposure']:.2f}")
    print(f"  Exposure percentage: {risk_report['exposure_pct']:.2f}%")
    print(f"  Open positions: {risk_report['open_positions']}")
    print(f"  Win rate: {risk_report['win_rate']:.2f}%")
    print(f"  Average win: ${risk_report['avg_win']:.2f}")
    print(f"  Average loss: ${risk_report['avg_loss']:.2f}")
    print(f"  Risk-reward ratio: {risk_report['risk_reward']:.2f}")
    print(f"  Expectancy: ${risk_report['expectancy']:.2f}")
    print(f"  Risk status: {risk_report['risk_status']}")
    
    # Test loss prevention recommendations
    print("\nTesting loss prevention recommendations...")
    recommendations = loss_prevention.get_loss_prevention_recommendations(risk_report, market_conditions)
    
    print(f"✓ Generated loss prevention recommendations:")
    for i, recommendation in enumerate(recommendations, 1):
        print(f"  {i}. {recommendation}")
    
    print("\nLoss Prevention System test completed")

if __name__ == "__main__":
    test_loss_prevention()
