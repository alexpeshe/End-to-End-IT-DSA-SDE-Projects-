import yfinance as yf
import pandas as pd
from datetime import datetime

# List of cryptocurrency tickers to download
tickers = ['BTC-USD', 'LTC-USD', 'ETH-USD', 'XRP-USD', 'SOL-USD']

# Set the date range for historical data
end_date = datetime.now()
start_date = datetime(2019, 1, 1)  # Start from January 1, 2019

# Download and save data for each ticker separately
for ticker in tickers:
    try:
        # Download data for single ticker
        data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
        
        if not data.empty:
            # Reset index to make Date a column
            data = data.reset_index()
            
            # Convert Date to string in YYYY-MM-DD format
            data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
            
            # Round numeric columns to 2 decimal places
            numeric_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close']
            for col in numeric_columns:
                if col in data.columns:  # Check if column exists
                    try:
                        data[col] = data[col].astype(float).round(2)
                    except Exception as e:
                        print(f"Error converting {col} column for {ticker}: {e}")
            
            # Convert Volume to integer
            if 'Volume' in data.columns:
                try:
                    data['Volume'] = data['Volume'].fillna(0).astype(int)
                except Exception as e:
                    print(f"Error converting Volume column for {ticker}: {e}")
            
            # Create filename using the ticker symbol
            filename = f"{ticker.split('-')[0]}_data.csv"
            
            # Save to CSV
            data.to_csv(filename, index=False)
            print(f"Data for {ticker} has been saved to {filename}")
        else:
            print(f"No data was downloaded for {ticker}")
            
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

print("Process completed.")