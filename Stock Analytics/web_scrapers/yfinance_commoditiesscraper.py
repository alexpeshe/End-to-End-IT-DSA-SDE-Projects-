import yfinance as yf
import pandas as pd
from datetime import datetime

# Dictionary of precious metal tickers and their names
metal_tickers = {
    'GC=F': 'Gold',
    'SI=F': 'Silver',
    'PL=F': 'Platinum',
    'PA=F': 'Palladium'
}

# Set the date range for historical data
end_date = datetime.now()
start_date = datetime(2019, 1, 1)  # Start from January 1, 2019

# Download and process data for each metal separately
for ticker, metal_name in metal_tickers.items():
    try:
        # Download data for single ticker
        print(f"Downloading data for {metal_name}...")
        data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
        
        if not data.empty:
            # Reset index to make Date a column
            data = data.reset_index()
            
            # Add Metal column
            data['Metal'] = metal_name
            
            # Convert Date to string in YYYY-MM-DD format
            data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
            
            # Round numeric columns to 2 decimal places
            numeric_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close']
            for col in numeric_columns:
                if col in data.columns:
                    try:
                        data[col] = data[col].astype(float).round(2)
                    except Exception as e:
                        print(f"Error converting {col} column for {metal_name}: {e}")
            
            # Convert Volume to integer
            if 'Volume' in data.columns:
                try:
                    data['Volume'] = data['Volume'].fillna(0).astype(int)
                except Exception as e:
                    print(f"Error converting Volume column for {metal_name}: {e}")
            
            # Reorder columns
            column_order = ['Date', 'Metal', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            data = data[column_order]
            
            # Create filename
            filename = f"{metal_name.lower()}_futures_data.csv"
            
            # Save to CSV
            data.to_csv(filename, index=False)
            print(f"Data for {metal_name} has been saved to {filename}")
            
            # Display first few rows as confirmation
            print(f"\nFirst few rows of {metal_name} data:")
            print(data.head())
            print("\n" + "="*50 + "\n")
            
        else:
            print(f"No data was downloaded for {metal_name}")
            
    except Exception as e:
        print(f"Error processing {metal_name}: {e}")

print("Process completed.")