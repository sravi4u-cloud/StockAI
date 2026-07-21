import pandas as pd
from database.db_manager import add_to_portfolio
from datetime import datetime

def import_portfolio_from_excel(file_path):
    try:
        # Read Excel file
        df = pd.read_excel(file_path)

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()

        # Check required columns
        required_columns = ['symbol', 'quantity', 'buy_price']

        for col in required_columns:
            if col not in df.columns:
                print(f"Missing column: {col}")
                return

        imported = 0

        # Add each row to portfolio
        for _, row in df.iterrows():
            symbol = str(row['symbol']).strip().upper()

            # Add .NS suffix if missing
            if not symbol.endswith(".NS"):
                symbol += ".NS"

            quantity = int(row['quantity'])
            buy_price = float(row['buy_price'])

            # Handle missing buy_date
            if 'buy_date' in df.columns and pd.notna(row['buy_date']):
                buy_date = pd.to_datetime(row['buy_date']).strftime("%Y-%m-%d")
            else:
                buy_date = datetime.now().strftime("%Y-%m-%d")

            add_to_portfolio(symbol, quantity, buy_price, buy_date)
            imported += 1

        print(f"Successfully imported {imported} holdings from Excel!")

    except Exception as e:
        print(f"Error importing Excel file: {e}")