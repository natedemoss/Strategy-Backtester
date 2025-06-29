import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from data.fetch_data import fetch_historical_data
from strategy.sma_crossover import calculate_signals
from backtest.backtester import Backtester
import altair as alt
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
st.set_page_config(page_title="SMA Crossover Backtester", layout="wide")

st.title("📈 Moving Average Crossover Strategy Backtester")
st.markdown("""
A simple app for backtesting the classic SMA crossover strategy.
""")

with st.sidebar:
    st.header("⚙️ Configuration")
    ticker = st.text_input("Stock Ticker (e.g. AAPL)", value="AAPL")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2024-01-01"))
    short_ma = st.number_input("Short MA Days", min_value=1, max_value=500, value=50)
    long_ma = st.number_input("Long MA Days", min_value=1, max_value=500, value=200)
    trade_qty = st.number_input("Trade Quantity", min_value=1, max_value=10000, value=10)
    run = st.button("🚀 Run Backtest")



if run:
    os.environ["ALPHA_VANTAGE_API_KEY"] = API_KEY
    try:
        st.info("Fetching historical data...")
        data = fetch_historical_data(
            ticker,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        st.success(f"Downloaded {len(data)} days of data.")

        st.divider()
        st.subheader(f"Summary for {ticker.upper()} | {start_date} to {end_date}")
        st.markdown(f"**Short MA:** {short_ma} days &nbsp;&nbsp;|&nbsp;&nbsp; **Long MA:** {long_ma} days &nbsp;&nbsp;|&nbsp;&nbsp; **Trade Size:** {trade_qty} shares")

        st.info("Calculating trading signals...")
        data = calculate_signals(data, int(short_ma), int(long_ma))
        st.success("Signals calculated.")

        st.divider()
        st.subheader("🔁 Backtest Results")
        backtester = Backtester(data, int(trade_qty))
        results = backtester.run()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Final Balance", f"${results['final_balance']:,.2f}", delta=f"${results['final_balance']-results['initial_balance']:,.2f}")
        col2.metric("Total Return", f"{results['total_return']}%")
        col3.metric("Total Trades", results['total_trades'])
        col4.metric("Win Rate", f"{results['win_rate']}%")

        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Max Drawdown", f"${results['max_drawdown']:,.2f}")
        col6.metric("Avg Profit/Trade", f"${results['avg_profit_per_trade']:,.2f}")
        col7.metric("Best Trade", f"${results['best_trade']:,.2f}")
        col8.metric("Worst Trade", f"${results['worst_trade']:,.2f}")

        st.divider()
        st.subheader("📈 Equity Curve")
        if hasattr(backtester, "portfolio_values") and backtester.portfolio_values:
            eq_df = pd.DataFrame(backtester.portfolio_values)
            eq_df["date"] = pd.to_datetime(eq_df["date"])
            eq_df = eq_df.set_index("date")
            st.line_chart(eq_df["value"], use_container_width=True)

        st.divider()
        st.subheader("📝 Trade Log")
        if backtester.trades:
            trades_df = pd.DataFrame(backtester.trades)
            trades_df['Profit'] = trades_df['profit'].round(2)
            trades_df['Result'] = np.where(trades_df['Profit'] > 0, 'Win', 'Loss')
            show_df = trades_df[['entry_date', 'exit_date', 'entry_price', 'exit_price', 'quantity', 'Profit', 'Result']]
            def profit_color(val):
                if val > 0:
                    return 'background-color: #198754; color: white;'
                elif val < 0:
                    return 'background-color: #dc3545; color: white;'
                else:
                    return ''
            st.dataframe(show_df.style.applymap(profit_color, subset=['Profit']), use_container_width=True)
        else:
            st.info("No trades executed during this period.")

        st.divider()
        with st.expander("Show Raw Data Table"):
            st.dataframe(data.tail(30), use_container_width=True)

        st.markdown("""
        ---
        **Strategy Tips:**
        - Try different MA periods for more or fewer trades
        - Adjust trade size based on your risk tolerance
        - Test different stocks to find the best performers
        """)

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("If you're seeing rate limit errors, please wait a few minutes and try again.")

# --- Footer ---
st.markdown('<div class="footer"> <a href="https://github.com/natedemoss/Strategy-Backtester" target="_blank">GitHub</a> &nbsp;|&nbsp; Made for LaunchHacks IV by Nathan DeMoss</div>', unsafe_allow_html=True) 