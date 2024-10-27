import yfinance as yf
import pandas as pd
from datetime import datetime

# List of stock tickers to download
tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM']

# Set the date range for historical data
start_date = '2019-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')  # Use current date to get latest data

# Download data for each ticker and save as separate CSV files
for ticker in tickers:
    print(f"Downloading data for {ticker}")
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            # Convert index to timezone-naive
            data.index = data.index.tz_localize(None)
            
            # Reset index to make Date a column
            data.reset_index(inplace=True)
            data.rename(columns={'index': 'Date'}, inplace=True)
            
            # Format the Date column
            data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
            
            # Save to CSV
            output_file = f'{ticker}_stock_data.csv'
            data.to_csv(output_file, index=False)
            print(f"Data for {ticker} has been downloaded and saved to {output_file}")
        else:
            print(f"No data available for {ticker}")
    except Exception as e:
        print(f"Error downloading data for {ticker}: {str(e)}")

print("Process completed.")