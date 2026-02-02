# Composite Equity Performance Graph

An interactive web app to visualize weighted portfolio performance of stocks and ETFs with real-time data from Yahoo Finance.

## Features

- **Up to 10 equities** - Select from popular stocks/ETFs or enter any custom symbol
- **Proportional weights** - Enter any numbers (1, 2, 3 or 50, 100, 200) - automatically scales to 100%
- **Real-time data** - Fetches live prices from Yahoo Finance
- **Custom date range** - Default: Jan 1, 2025 to today
- **Smart frequency selection** - Automatically chooses daily/weekly/monthly to keep <100 samples
- **Manual frequency override** - Choose daily, weekly, or monthly regardless of date range
- **0% baseline** - All equities start at 0% for easy comparison
- **Composite line** - Shows weighted average performance (dashed white line)
- **Period returns** - Displays % gain/loss for each equity

## Quick Start

Simply open `index.html` in your web browser. The app will automatically fetch real market data from Yahoo Finance.

**Note:** If real data fails to load (network issues, invalid symbol), the app falls back to simulated data and shows a warning.

## Frequency Selection

The app **automatically selects the best frequency** based on your date range to keep data points under 100 per equity (reducing noise and improving performance):

- **Daily**: Used for date ranges ≤ 100 trading days (~5 months)
- **Weekly**: Used for date ranges ~100-500 trading days (5 months - 2 years)
- **Monthly**: Used for date ranges > 500 trading days (2+ years)

You can **manually override** the automatic selection using the frequency dropdown in the app. The hints show the estimated sample count for reference.

## Files

| File | Description |
|------|-------------|
| `index.html` | Main web app (use this for GitHub Pages) |
| `app.html` | Development version |
| `fetch_data.py` | Python script for local data fetching with frequency selection |
| `README.md` | This documentation |

## How Weights Work

Enter any proportional numbers - the app auto-calculates percentages:

| You Enter | Calculated Weight |
|-----------|-------------------|
| 1, 1, 1 | 33.3%, 33.3%, 33.3% |
| 2, 1, 1 | 50%, 25%, 25% |
| 3, 2, 1 | 50%, 33.3%, 16.7% |
| 100, 50, 50 | 50%, 25%, 25% |

## Available Equities

**ETFs:** SPY, QQQ, DIA, IWM, VTI

**Tech:** AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, AMD, AVGO, CRM

**Finance:** JPM, V, MA, BRK-B

**Healthcare:** JNJ, UNH

**Consumer:** HD, PG, COST

**Energy:** XOM

**Custom:** Type any valid stock symbol in the input field

## Using the Python Data Fetcher

For more control over data fetching, use `fetch_data.py`:

```bash
# Auto-select frequency based on date range
python fetch_data.py --start 2024-01-01 --end 2025-01-31

# Force a specific frequency
python fetch_data.py --frequency daily
python fetch_data.py --frequency weekly
python fetch_data.py --frequency monthly

# Custom symbols and weights
python fetch_data.py --symbols SPY QQQ AAPL --start 2023-01-01 --frequency weekly --weights 40 35 25
```

The script automatically selects the highest frequency (daily → weekly → monthly) that keeps samples below 100. You can override this with `--frequency`.

Output is saved as `stock_data.json` (or specify with `--output`).

## Deploy to GitHub Pages

1. Create a new repository on GitHub
2. Upload `index.html` and `README.md`
3. Go to Settings → Pages → Deploy from main branch
4. Your app will be live at `https://YOUR-USERNAME.github.io/REPO-NAME/`

## Tech Stack

- Chart.js 4.4 (charting)
- Yahoo Finance API (real-time data via CORS proxy)
- Pure HTML/CSS/JavaScript (no build step)

## Troubleshooting

**"Using simulated data" warning?**
- Check if the stock symbol is valid
- The CORS proxy may be temporarily down - try refreshing
- Some symbols (especially non-US) may not be available

**Chart not loading?**
- Ensure you have an internet connection
- Try a different browser
- Check browser console for errors
