# Composite Equity Performance Graph

An interactive web app to visualize weighted portfolio performance of stocks and ETFs with real-time data from Yahoo Finance.

## Features

- **Up to 10 equities** - Select from popular stocks/ETFs or enter any custom symbol
- **Proportional weights** - Enter any numbers (1, 2, 3 or 50, 100, 200) - automatically scales to 100%
- **Real-time data** - Fetches live prices from Yahoo Finance
- **Custom date range** - Default: Jan 1, 2025 to today
- **0% baseline** - All equities start at 0% for easy comparison
- **Composite line** - Shows weighted average performance (dashed white line)
- **Period returns** - Displays % gain/loss for each equity

## Quick Start

Simply open `index.html` in your web browser. The app will automatically fetch real market data from Yahoo Finance.

**Note:** If real data fails to load (network issues, invalid symbol), the app falls back to simulated data and shows a warning.

## Files

| File | Description |
|------|-------------|
| `index.html` | Main web app (use this for GitHub Pages) |
| `app.html` | Development version |
| `fetch_data.py` | Python script for local data fetching (optional) |
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
