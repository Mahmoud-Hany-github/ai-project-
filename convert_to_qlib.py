import pandas as pd
import os

def convert_to_qlib_format(input_csv, output_dir):
    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Ensure required columns exist (adjust based on your data)
    required_columns = ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']

    for _, row in data.iterrows():
        symbol = row["Symbol"]
        symbol_dir = os.path.join(output_dir, symbol)
        os.makedirs(symbol_dir, exist_ok=True)

        row_data = row[["Date", "Open", "High", "Low", "Close", "Volume"]]
        output_path = os.path.join(symbol_dir, f"{symbol}.csv")
        row_data.to_csv(output_path, index=False)

    # Reformat the date to YYYY-MM-DD if necessary
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Group by symbol and save each symbol's data as a separate CSV
    for symbol, group in df.groupby('Symbol'):
        group = group.sort_values('Date')  # Ensure data is sorted by date
        symbol_path = os.path.join(output_dir, f"{symbol}.csv")
        group.to_csv(symbol_path, index=False)
        print(f"Saved data for {symbol} to {symbol_path}")

if __name__ == "__main__":
    input_csv = "api_results.csv"  # Path to your input CSV
    output_dir = "./qlib_data"    # Path to save Qlib-compatible data
    convert_to_qlib_format(input_csv, output_dir)


