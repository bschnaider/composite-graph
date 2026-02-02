#!/usr/bin/env python3
"""
Composite Equity Performance - Data Fetcher
Fetches real stock data from Yahoo Finance and outputs JSON for the web app.

Usage:
    python fetch_data.py
    python fetch_data.py --symbols SPY QQQ AAPL --start 2025-01-01 --end 2025-01-31
    python fetch_data.py --frequency daily
    python fetch_data.py --start 2020-01-01 --end 2025-01-31 --frequency weekly

Frequency Selection:
    - If --frequency is not specified, automatically selects the highest resolution
      (daily → weekly → monthly) such that samples < 100 per equity
    - User can override with --frequency daily|weekly|monthly
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("Required packages not installed. Run:")
    print("  pip install yfinance pandas --break-system-packages")
    exit(1)


def calculate_optimal_frequency(start_date: str, end_date: str, max_samples: int = 100) -> str:
    """
    Determine the optimal frequency (daily, weekly, monthly) to keep samples under max_samples.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        max_samples: Maximum number of samples allowed (default 100)

    Returns:
        Optimal frequency: 'daily', 'weekly', or 'monthly'
    """
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    # Estimate trading days (~252 per year, ~5 per week, ~21 per month)
    days_diff = (end - start).days
    estimated_trading_days = int(days_diff * 252 / 365)
    estimated_weeks = estimated_trading_days / 5
    estimated_months = estimated_trading_days / 21

    if estimated_trading_days <= max_samples:
        return 'daily'
    elif estimated_weeks <= max_samples:
        return 'weekly'
    else:
        return 'monthly'


def resample_data(data: list, frequency: str) -> list:
    """
    Resample data to specified frequency while maintaining normalized values.

    Args:
        data: List of daily data points
        frequency: 'daily', 'weekly', or 'monthly'

    Returns:
        Resampled data list
    """
    if frequency == 'daily':
        return data

    if not data:
        return data

    # Convert to DataFrame for easier resampling
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Resample: take the last value of each period
    if frequency == 'weekly':
        resampled = df.resample('W').last()
    elif frequency == 'monthly':
        resampled = df.resample('M').last()
    else:
        return data

    # Remove NaN rows and convert back to list
    resampled = resampled.dropna(how='all')
    result = []
    for date, row in resampled.iterrows():
        entry = {'date': date.strftime('%Y-%m-%d')}
        for col in row.index:
            if col != 'date' and pd.notna(row[col]):
                entry[col] = round(row[col], 2)
        if len(entry) > 1:
            result.append(entry)

    return result


def fetch_equity_data(symbols: list, start_date: str, end_date: str, frequency: str = 'daily') -> dict:
    """
    Fetch historical price data for given symbols and normalize to start at 100.

    Args:
        symbols: List of stock/ETF symbols (e.g., ['SPY', 'QQQ', 'AAPL'])
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        frequency: 'daily', 'weekly', or 'monthly'

    Returns:
        Dictionary with dates as keys and normalized prices for each symbol
    """
    print(f"Fetching data for {symbols} from {start_date} to {end_date}...")
    print(f"Frequency: {frequency}")

    # Download data for all symbols at once
    data = yf.download(
        symbols,
        start=start_date,
        end=end_date,
        progress=False,
        auto_adjust=True
    )

    # Handle single symbol case (different DataFrame structure)
    if len(symbols) == 1:
        close_prices = data['Close'].to_frame(name=symbols[0])
    else:
        close_prices = data['Close']

    # Normalize: each series starts at 100
    normalized = pd.DataFrame()
    for symbol in symbols:
        if symbol in close_prices.columns:
            series = close_prices[symbol].dropna()
            if len(series) > 0:
                start_price = series.iloc[0]
                normalized[symbol] = (series / start_price) * 100

    # Convert to list of dictionaries for JSON
    result = []
    for date, row in normalized.iterrows():
        entry = {'date': date.strftime('%Y-%m-%d')}
        for symbol in symbols:
            if symbol in row and pd.notna(row[symbol]):
                entry[symbol] = round(row[symbol], 2)
        if len(entry) > 1:  # Has at least one symbol
            result.append(entry)

    # Resample to desired frequency
    result = resample_data(result, frequency)

    return result


def calculate_composite(data: list, weights: dict) -> list:
    """
    Calculate weighted composite performance.

    Args:
        data: List of daily data points with normalized prices
        weights: Dictionary mapping symbol to weight (0-100)

    Returns:
        Data with added 'Composite' field
    """
    total_weight = sum(weights.values())
    if total_weight == 0:
        return data

    for point in data:
        composite = 0
        for symbol, weight in weights.items():
            if symbol in point:
                composite += point[symbol] * (weight / total_weight)
        point['Composite'] = round(composite, 2)

    return data


def main():
    parser = argparse.ArgumentParser(description='Fetch equity data from Yahoo Finance')
    parser.add_argument('--symbols', nargs='+', default=['SPY', 'QQQ', 'AAPL', 'MSFT', 'NVDA'],
                        help='Stock symbols to fetch')
    parser.add_argument('--start', default='2025-01-01',
                        help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', default=datetime.now().strftime('%Y-%m-%d'),
                        help='End date (YYYY-MM-DD)')
    parser.add_argument('--frequency', default=None, choices=['daily', 'weekly', 'monthly'],
                        help='Data frequency (daily, weekly, monthly). If not specified, auto-selects to keep <100 samples')
    parser.add_argument('--weights', nargs='+', type=float, default=None,
                        help='Weights for each symbol (must match number of symbols)')
    parser.add_argument('--output', default='stock_data.json',
                        help='Output JSON file path')

    args = parser.parse_args()

    # Auto-select frequency if not specified
    if args.frequency is None:
        args.frequency = calculate_optimal_frequency(args.start, args.end, max_samples=100)
        print(f"📊 Auto-selected frequency: {args.frequency} (to keep samples < 100)")
    else:
        print(f"📊 Using specified frequency: {args.frequency}")

    # Fetch the data
    data = fetch_equity_data(args.symbols, args.start, args.end, frequency=args.frequency)

    if not data:
        print("No data retrieved. Check your symbols and date range.")
        return

    # Calculate composite if weights provided
    if args.weights:
        if len(args.weights) != len(args.symbols):
            print(f"Warning: {len(args.weights)} weights provided for {len(args.symbols)} symbols")
            weights = {s: 100/len(args.symbols) for s in args.symbols}
        else:
            weights = dict(zip(args.symbols, args.weights))
    else:
        # Equal weights
        weights = {s: 100/len(args.symbols) for s in args.symbols}

    data = calculate_composite(data, weights)

    # Save to JSON
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump({
            'symbols': args.symbols,
            'weights': weights,
            'start_date': args.start,
            'end_date': args.end,
            'data': data
        }, f, indent=2)

    print(f"\n✅ Data saved to {output_path}")
    print(f"   {len(data)} trading days fetched")
    print(f"   Symbols: {', '.join(args.symbols)}")
    print(f"   Weights: {weights}")

    # Show sample
    if len(data) > 0:
        print(f"\n📊 Sample (first day):")
        print(f"   {data[0]}")
        print(f"\n📊 Sample (last day):")
        print(f"   {data[-1]}")


if __name__ == '__main__':
    main()
