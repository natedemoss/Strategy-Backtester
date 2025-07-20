# Strategy Backtester

A Python-based tool for backtesting trading strategies on historical stock data. Fetches data from Alpha Vantage and provides both a command-line and optional Streamlit web interface.

## Features

- Fetch historical stock data using Alpha Vantage
- Backtest custom trading strategies
- Analyze results with performance metrics
- Optional Streamlit web app for interactive analysis

## Requirements

- Python 3.8+
- Alpha Vantage API key (free at [Alpha Vantage](http s://www.alphavantage.co/support/#api-key))

### Python Libraries Used

| Library           | Purpose                                      |
|-------------------|----------------------------------------------|
| pandas            | Data analysis and manipulation               |
| numpy             | Numerical calculations                       |
| python-dotenv     | Load environment variables from `.env` files |
| alpha_vantage     | Fetch historical stock data                  |
| streamlit         | Web app interface (optional)                 |
| altair            | Charting in Streamlit app (optional)         |

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/Strategy-Backtester.git
   cd Strategy-Backtester
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

   If you want to use the Streamlit app:
   ```sh
   pip install streamlit altair
   ```

3. **Set up your Alpha Vantage API key:**
   - Create a `.env` or `config.env` file in the project root:
     ```
     ALPHA_VANTAGE_API_KEY=your_api_key_here
     ```

## Usage

### Command Line

Run the main script to backtest a strategy:
```sh
python main.py
```

### Streamlit Web App (Optional)

Start the web app:
```sh
streamlit run streamlit_app.py
```

## File Structure

- `main.py` — Main entry point for running backtests
- `data/fetch_data.py` — Fetches historical data from Alpha Vantage
- `backtest/backtester.py` — Core backtesting logic
- `strategies/` — Example trading strategies
- `streamlit_app.py` — Streamlit web interface (optional)
- `requirements.txt` — Python dependencies

## Notes

- Only Alpha Vantage is supported for data fetching in this version.
- If you want to use other data sources (like yfinance), you’ll need to modify the code.

## License

MIT
