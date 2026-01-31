# Composite Equity Performance Graph

An interactive web app to visualize weighted portfolio performance of up to 5 stocks/ETFs.

## Features

- **Select up to 5 equities** from a dropdown of popular stocks and ETFs
- **Adjust weights** for each equity (default: equal weight)
- **Custom date range** (default: Jan 1, 2025 to today)
- **Normalized performance** - all equities start at 100 for easy comparison
- **Composite line** - shows weighted average performance
- **Period returns** - displays % gain/loss for each equity

## Quick Start

### Option 1: Open directly (uses simulated data)
Simply open `app.html` in your web browser. It will use realistic simulated data.

### Option 2: Use real Yahoo Finance data
1. Install dependencies:
   ```bash
   pip install yfinance pandas
   ```

2. Fetch real stock data:
   ```bash
   python fetch_data.py
   ```
   This creates `stock_data.json` with real market data.

3. Start a local server:
   ```bash
   python -m http.server 8000
   ```

4. Open in browser:
   ```
   http://localhost:8000/app.html
   ```

## Customizing Data Fetch

```bash
# Custom symbols
python fetch_data.py --symbols SPY QQQ AAPL GOOGL AMZN

# Custom date range
python fetch_data.py --start 2024-06-01 --end 2024-12-31

# Custom weights
python fetch_data.py --symbols SPY QQQ --weights 60 40

# Save to different file
python fetch_data.py --output my_portfolio.json
```

## Files

| File | Description |
|------|-------------|
| `app.html` | Main web app - opens in any browser |
| `index.html` | Alternate version (standalone demo) |
| `fetch_data.py` | Python script to get real Yahoo Finance data |
| `stock_data.json` | Generated data file (after running fetch_data.py) |

## Available Equities

The app includes 25+ popular stocks and ETFs:

**ETFs:** SPY, QQQ, DIA, IWM, VTI

**Tech:** AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, AMD, AVGO, CRM

**Finance:** JPM, V, MA, BRK-B

**Healthcare:** JNJ, UNH

**Consumer:** HD, PG, COST

**Energy:** XOM

## How It Works

1. **Normalization**: Each equity's price is converted to start at 100 on the first date
2. **Weighting**: The composite is calculated as the weighted average of normalized prices
3. **Visualization**: Recharts renders an interactive line chart with tooltips and legend

## Tech Stack

- React 18 (via CDN)
- Recharts (charting library)
- yfinance (Python, for real data)
- Pure HTML/CSS (no build step required)
