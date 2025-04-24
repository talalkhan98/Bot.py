import pandas as pd
import numpy as np

class LossPreventionSystem:
    """
    A class for implementing loss prevention features in the crypto trading bot.
    These features help protect users from significant losses in volatile crypto markets.
    """
    
    def __init__(self):
        """Initialize the LossPreventionSystem."""
        # Default risk parameters
        self.max_position_size_pct = 5.0  # Maximum position size as percentage of portfolio
        self.max_risk_per_trade_pct = 2.0  # Maximum risk per trade as percentage of portfolio
        self.max_daily_loss_pct = 5.0  # Maximum daily loss as percentage of portfolio
        self.max_drawdown_pct = 15.0  # Maximum drawdown as percentage of portfolio
        self.trailing_stop_pct = 2.0  # Trailing stop percentage
        self.volatility_adjustment = True  # Whether to adjust position size based on volatility
        self.correlation_filter = True  # Whether to filter trades based on correlation
        self.max_open_positions = 3  # Maximum number of open positions
        
    def set_risk_parameters(self, **kwargs):
        """
        Set risk parameters for the loss prevention system.
        
        Args:
            **kwargs: Risk parameters to set
        """
        if 'max_position_size_pct' in kwargs:
            self.max_position_size_pct = kwargs['max_position_size_pct']
        if 'max_risk_per_trade_pct' in kwargs:
            self.max_risk_per_trade_pct = kwargs['max_risk_per_trade_pct']
        if 'max_daily_loss_pct' in kwargs:
            self.max_daily_loss_pct = kwargs['max_daily_loss_pct']
        if 'max_drawdown_pct' in kwargs:
            self.max_drawdown_pct = kwargs['max_drawdown_pct']
        if 'trailing_stop_pct' in kwargs:
            self.trailing_stop_pct = kwargs['trailing_stop_pct']
        if 'volatility_adjustment' in kwargs:
            self.volatility_adjustment = kwargs['volatility_adjustment']
        if 'correlation_filter' in kwargs:
            self.correlation_filter = kwargs['correlation_filter']
        if 'max_open_positions' in kwargs:
            self.max_open_positions = kwargs['max_open_positions']
    
    def calculate_position_size(self, account_balance, entry_price, stop_loss, volatility=None):
        """
        Calculate position size based on risk parameters.
        
        Args:
            account_balance (float): Account balance
            entry_price (float): Entry price
            stop_loss (float): Stop loss price
            volatility (float, optional): Asset volatility
            
        Returns:
            float: Position size in units
        """
        # Calculate risk amount
        risk_amount = account_balance * (self.max_risk_per_trade_pct / 100)
        
        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_loss)
        
        if risk_per_unit == 0:
            return 0
        
        # Calculate position size
        position_size = risk_amount / risk_per_unit
        
        # Adjust position size based on volatility
        if self.volatility_adjustment and volatility is not None:
            # Reduce position size for high volatility assets
            volatility_factor = 1 / (1 + volatility)
            position_size *= volatility_factor
        
        # Ensure position size doesn't exceed maximum
        max_position_size = account_balance * (self.max_position_size_pct / 100) / entry_price
        position_size = min(position_size, max_position_size)
        
        return position_size
    
    def calculate_stop_loss(self, entry_price, direction, atr=None, fixed_pct=None):
        """
        Calculate stop loss price based on risk parameters.
        
        Args:
            entry_price (float): Entry price
            direction (int): Trade direction (1 for long, -1 for short)
            atr (float, optional): Average True Range
            fixed_pct (float, optional): Fixed percentage for stop loss
            
        Returns:
            float: Stop loss price
        """
        if fixed_pct is not None:
            # Use fixed percentage stop loss
            stop_pct = fixed_pct
        elif atr is not None:
            # Use ATR-based stop loss (2 * ATR)
            stop_pct = (2 * atr / entry_price) * 100
        else:
            # Use default stop loss percentage
            stop_pct = 5.0
        
        # Calculate stop loss price
        if direction == 1:  # Long position
            stop_loss = entry_price * (1 - stop_pct / 100)
        else:  # Short position
            stop_loss = entry_price * (1 + stop_pct / 100)
        
        return stop_loss
    
    def calculate_take_profit(self, entry_price, stop_loss, direction, risk_reward_ratio=2.0):
        """
        Calculate take profit price based on risk parameters.
        
        Args:
            entry_price (float): Entry price
            stop_loss (float): Stop loss price
            direction (int): Trade direction (1 for long, -1 for short)
            risk_reward_ratio (float): Risk-reward ratio
            
        Returns:
            float: Take profit price
        """
        # Calculate risk
        risk = abs(entry_price - stop_loss)
        
        # Calculate reward
        reward = risk * risk_reward_ratio
        
        # Calculate take profit price
        if direction == 1:  # Long position
            take_profit = entry_price + reward
        else:  # Short position
            take_profit = entry_price - reward
        
        return take_profit
    
    def update_trailing_stop(self, entry_price, current_price, current_stop, direction):
        """
        Update trailing stop price.
        
        Args:
            entry_price (float): Entry price
            current_price (float): Current price
            current_stop (float): Current stop loss price
            direction (int): Trade direction (1 for long, -1 for short)
            
        Returns:
            float: Updated stop loss price
        """
        if direction == 1:  # Long position
            # Calculate trailing stop price
            trailing_stop = current_price * (1 - self.trailing_stop_pct / 100)
            
            # Only update if trailing stop is higher than current stop
            if trailing_stop > current_stop:
                return trailing_stop
            else:
                return current_stop
        else:  # Short position
            # Calculate trailing stop price
            trailing_stop = current_price * (1 + self.trailing_stop_pct / 100)
            
            # Only update if trailing stop is lower than current stop
            if trailing_stop < current_stop:
                return trailing_stop
            else:
                return current_stop
    
    def check_max_daily_loss(self, daily_pnl, account_balance):
        """
        Check if maximum daily loss has been reached.
        
        Args:
            daily_pnl (float): Daily profit/loss
            account_balance (float): Account balance
            
        Returns:
            bool: True if maximum daily loss has been reached, False otherwise
        """
        daily_loss_pct = (daily_pnl / account_balance) * 100
        
        return daily_loss_pct <= -self.max_daily_loss_pct
    
    def check_max_drawdown(self, current_balance, peak_balance):
        """
        Check if maximum drawdown has been reached.
        
        Args:
            current_balance (float): Current account balance
            peak_balance (float): Peak account balance
            
        Returns:
            bool: True if maximum drawdown has been reached, False otherwise
        """
        drawdown_pct = ((current_balance - peak_balance) / peak_balance) * 100
        
        return drawdown_pct <= -self.max_drawdown_pct
    
    def filter_correlated_assets(self, correlation_matrix, threshold=0.7):
        """
        Filter highly correlated assets to avoid overexposure.
        
        Args:
            correlation_matrix (pd.DataFrame): Correlation matrix
            threshold (float): Correlation threshold
            
        Returns:
            list: List of asset pairs to avoid trading simultaneously
        """
        highly_correlated = []
        
        # Get upper triangle of correlation matrix
        upper = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
        
        # Find pairs with correlation above threshold
        for col in upper.columns:
            for idx, value in upper[col].items():
                if value > threshold:
                    highly_correlated.append((idx, col))
        
        return highly_correlated
    
    def check_market_conditions(self, df, lookback=20):
        """
        Check market conditions to adjust risk parameters.
        
        Args:
            df (pd.DataFrame): DataFrame with price data
            lookback (int): Lookback period
            
        Returns:
            dict: Market condition assessment
        """
        # Calculate recent volatility
        returns = df['close'].pct_change().dropna()
        recent_volatility = returns[-lookback:].std() * np.sqrt(252)  # Annualized
        
        # Calculate trend strength
        if 'adx_14' in df.columns:
            trend_strength = df['adx_14'].iloc[-1]
        else:
            trend_strength = None
        
        # Determine market regime
        if recent_volatility > 0.8:  # High volatility
            market_regime = "High Volatility"
            risk_factor = 0.5  # Reduce risk
        elif trend_strength is not None and trend_strength > 25:  # Strong trend
            market_regime = "Strong Trend"
            risk_factor = 1.0  # Normal risk
        else:  # Normal conditions
            market_regime = "Normal"
            risk_factor = 0.75  # Moderate risk
        
        return {
            'market_regime': market_regime,
            'volatility': recent_volatility,
            'trend_strength': trend_strength,
            'risk_factor': risk_factor
        }
    
    def adjust_risk_for_market_conditions(self, market_conditions):
        """
        Adjust risk parameters based on market conditions.
        
        Args:
            market_conditions (dict): Market condition assessment
            
        Returns:
            dict: Adjusted risk parameters
        """
        risk_factor = market_conditions['risk_factor']
        
        # Adjust risk parameters
        adjusted_params = {
            'max_position_size_pct': self.max_position_size_pct * risk_factor,
            'max_risk_per_trade_pct': self.max_risk_per_trade_pct * risk_factor,
            'trailing_stop_pct': self.trailing_stop_pct * (2 - risk_factor)  # Tighter stops in high volatility
        }
        
        return adjusted_params
    
    def generate_risk_report(self, trades, account_balance, open_positions):
        """
        Generate risk report.
        
        Args:
            trades (pd.DataFrame): DataFrame with trade history
            account_balance (float): Current account balance
            open_positions (list): List of open positions
            
        Returns:
            dict: Risk report
        """
        # Calculate total exposure
        total_exposure = sum(pos['value'] for pos in open_positions) if open_positions else 0
        exposure_pct = (total_exposure / account_balance) * 100
        
        # Calculate win rate
        if len(trades) > 0:
            winning_trades = trades[trades['profit_loss'] > 0]
            win_rate = len(winning_trades) / len(trades) * 100
        else:
            win_rate = 0
        
        # Calculate average win and loss
        avg_win = winning_trades['profit_loss'].mean() if len(winning_trades) > 0 else 0
        losing_trades = trades[trades['profit_loss'] < 0]
        avg_loss = losing_trades['profit_loss'].mean() if len(losing_trades) > 0 else 0
        
        # Calculate risk-reward ratio
        risk_reward = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        
        # Calculate expectancy
        expectancy = (win_rate / 100 * avg_win) + ((100 - win_rate) / 100 * avg_loss)
        
        # Generate report
        report = {
            'total_exposure': total_exposure,
            'exposure_pct': exposure_pct,
            'open_positions': len(open_positions) if open_positions else 0,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'risk_reward': risk_reward,
            'expectancy': expectancy,
            'risk_status': 'High Risk' if exposure_pct > 50 else 'Medium Risk' if exposure_pct > 25 else 'Low Risk'
        }
        
        return report
    
    def get_loss_prevention_recommendations(self, risk_report, market_conditions):
        """
        Get loss prevention recommendations.
        
        Args:
            risk_report (dict): Risk report
            market_conditions (dict): Market condition assessment
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        # Check exposure
        if risk_report['exposure_pct'] > 50:
            recommendations.append("Reduce overall exposure to decrease risk.")
        
        # Check open positions
        if risk_report['open_positions'] >= self.max_open_positions:
            recommendations.append("Maximum number of open positions reached. Close some positions before opening new ones.")
        
        # Check win rate
        if risk_report['win_rate'] < 40:
            recommendations.append("Win rate is low. Consider adjusting your strategy or taking a break.")
        
        # Check risk-reward ratio
        if risk_report['risk_reward'] < 1:
            recommendations.append("Risk-reward ratio is unfavorable. Aim for larger profit targets or tighter stop losses.")
        
        # Check market conditions
        if market_conditions['market_regime'] == "High Volatility":
            recommendations.append("Market volatility is high. Reduce position sizes and use wider stop losses.")
        
        # Check expectancy
        if risk_report['expectancy'] < 0:
            recommendations.append("Trading expectancy is negative. Review your strategy or consider paper trading.")
        
        return recommendations
