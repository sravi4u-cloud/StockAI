import pandas as pd
from database.db_manager import add_to_portfolio

def import_portfolio_from_excel(file_path):
    try:
        # Read Excel file
        df = pd.read_excel(file_path)

        # Check required columns
        required_columns = ['symbol', 'quantity', 'buy_price', 'buy_date']

        for col in required_columns:
            if col not in df.columns:
                print(f"Missing column: {col}")
                return

        # Add each row to portfolio
        for _, row in df.iterrows():
            add_to_portfolio(
                symbol=str(row['symbol']).upper(),
                quantity=int(row['quantity']),
                buy_price=float(row['buy_price']),
                buy_date=str(row['buy_date'])[:10]
            )

        print(f"Successfully imported {len(df)} holdings from Excel!")

    except Exception as e:
        print(f"Error importing Excel file: {e}")