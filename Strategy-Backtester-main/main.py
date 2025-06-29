import os
from dotenv import load_dotenv
from data.fetch_data import fetch_historical_data
from strategy.sma_crossover import calculate_signals
from backtest.backtester import Backtester
import sys

def main():
    # Load configuration
    try:
        load_dotenv('config/config.env')
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        sys.exit(1)
    
    # Get configuration 
    try:
        ticker = os.getenv('TICKER')
        start_date = os.getenv('START_DATE')
        end_date = os.getenv('END_DATE')
        short_ma = int(os.getenv('SHORT_MA_DAYS'))
        long_ma = int(os.getenv('LONG_MA_DAYS'))
        trade_qty = int(os.getenv('TRADE_QTY'))
        
        if not all([ticker, start_date, end_date]):
            raise ValueError("Missing required configuration values")
            
    except Exception as e:
        print(f"Error reading configuration: {str(e)}")
        sys.exit(1)
    
    print(f"\n=== Moving Average Crossover Strategy Backtest ===")
    print(f"Stock: {ticker}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Strategy: {short_ma}-day MA crossing {long_ma}-day MA")
    print(f"Trade Size: {trade_qty} shares per trade\n")
    
    try:
        # Fetch data
        print("Fetching historical data (this may take a few moments)...")
        data = fetch_historical_data(ticker, start_date, end_date)
        print(f"Successfully downloaded {len(data)} days of data")
        
        # Calculate signals
        print("\nCalculating trading signals...")
        data = calculate_signals(data, short_ma, long_ma)
        
        # Run backtest
        print("\nRunning backtest simulation...")
        backtester = Backtester(data, trade_qty)
        results = backtester.run()
        
        # Print results
        print("\n=== Backtest Results ===")
        print(f"💰 Starting Balance: ${results['initial_balance']:,.2f}")
        print(f"💰 Final Balance: ${results['final_balance']:,.2f}")
        print(f"📈 Total Return: {results['total_return']}%")
        print(f"\n✅ Total Trades: {results['total_trades']}")
        print(f"💵 Total Profit: ${results['total_profit']:,.2f}")
        print(f"📈 Win Rate: {results['win_rate']}%")
        print(f"📉 Max Drawdown: ${results['max_drawdown']:,.2f}")
        print(f"💵 Average Profit per Trade: ${results['avg_profit_per_trade']:,.2f}")
        print(f"🏆 Best Trade: ${results['best_trade']:,.2f}")
        print(f"📉 Worst Trade: ${results['worst_trade']:,.2f}")
        
        # Print strategy tips
        print("\n=== Strategy Tips ===")
        print("• Try different MA periods in config.env:")
        print("  - Shorter periods (e.g., 10/30) = more trades, faster response")
        print("  - Longer periods (e.g., 50/200) = fewer trades, longer trends")
        print("• Adjust trade size (TRADE_QTY) based on your risk tolerance")
        print("• Test different stocks to find the best performers\n")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nIf you're seeing rate limit errors, please wait a few minutes and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 