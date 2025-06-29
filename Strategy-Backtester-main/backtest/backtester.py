import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class Backtester:
    def __init__(self, data: pd.DataFrame, trade_qty: int, initial_balance: float = 10000.0):
        self.data = data
        self.trade_qty = trade_qty
        self.positions: List[Dict] = []
        self.initial_balance = initial_balance
        self.cash = initial_balance
        self.trades = []
        self.portfolio_values = []  # Track portfolio value over time
        
    def run(self) -> Dict:
        """
        Run the backtest simulation.
        
        Returns:
            Dict: Dictionary containing backtest results
        """
        position_open = False
        current_position = None
        
        # Track portfolio value over time
        for index, row in self.data.iterrows():
            # Calculate current portfolio value
            position_value = 0
            if position_open and current_position:
                position_value = row['Close'] * current_position['quantity']
            portfolio_value = self.cash + position_value
            self.portfolio_values.append({
                'date': index,
                'value': portfolio_value
            })
            
            if row['signal'] == 1 and not position_open:  # Buy 
                current_position = self._execute_buy(index, row['Close'])
                position_open = True
            elif row['signal'] == -1 and position_open:  # Sell 
                self._execute_sell(index, row['Close'], current_position)
                position_open = False
                current_position = None
                
        # Close any open position at the end
        if position_open and current_position:
            self._execute_sell(self.data.index[-1], self.data['Close'].iloc[-1], current_position)
            
        return self._calculate_performance()
    
    def _execute_buy(self, date, price: float) -> Dict:
        """Execute a buy trade."""
        cost = price * self.trade_qty
        self.cash -= cost
        position = {
            'entry_date': date,
            'entry_price': price,
            'quantity': self.trade_qty
        }
        self.positions.append(position)
        return position
        
    def _execute_sell(self, date, price: float, position: Dict):
        """Execute a sell trade."""
        if not position:
            return
            
        revenue = price * position['quantity']
        self.cash += revenue
        
        # Record trade
        profit = revenue - (position['entry_price'] * position['quantity'])
        self.trades.append({
            'entry_date': position['entry_date'],
            'exit_date': date,
            'entry_price': position['entry_price'],
            'exit_price': price,
            'quantity': position['quantity'],
            'profit': profit
        })
        
    def _calculate_performance(self) -> Dict:
        """Calculate backtest performance metrics."""
        if not self.trades:
            return {
                'total_trades': 0,
                'total_profit': 0,
                'win_rate': 0,
                'max_drawdown': 0,
                'avg_profit_per_trade': 0,
                'best_trade': 0,
                'worst_trade': 0,
                'initial_balance': self.initial_balance,
                'final_balance': self.initial_balance,
                'total_return': 0
            }
            
        profits = [t['profit'] for t in self.trades]
        total_profit = sum(profits)
        winning_trades = sum(1 for p in profits if p > 0)
        win_rate = (winning_trades / len(self.trades)) * 100
        
        # Calculate max drawdown
        portfolio_values = [pv['value'] for pv in self.portfolio_values]
        max_drawdown = 0
        peak = portfolio_values[0]
        
        for value in portfolio_values:
            if value > peak:
                peak = value
            drawdown = peak - value
            max_drawdown = max(max_drawdown, drawdown)
        
        final_balance = self.initial_balance + total_profit
        total_return = ((final_balance - self.initial_balance) / self.initial_balance) * 100
        
        return {
            'total_trades': len(self.trades),
            'total_profit': round(total_profit, 2),
            'win_rate': round(win_rate, 2),
            'max_drawdown': round(max_drawdown, 2),
            'avg_profit_per_trade': round(np.mean(profits), 2),
            'best_trade': round(max(profits), 2),
            'worst_trade': round(min(profits), 2),
            'initial_balance': round(self.initial_balance, 2),
            'final_balance': round(final_balance, 2),
            'total_return': round(total_return, 2)
        } 