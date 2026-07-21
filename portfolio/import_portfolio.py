import pandas as pd
from database.database import get_connection

def import_portfolio_from_excel(file_path):
    # Read Excel file
    df = pd.read_excel(file_path)

    conn = get_connection()
    cursor = conn.cursor()

    imported = 0

    for _, row in df.iterrows():
        symbol = str(row["Symbol"]).upper()
        quantity = float(row["Qty"])
        buy_price = float(row["Buy Price"])

        cursor.execute(
            "INSERT INTO portfolio (symbol, quantity, buy_price) VALUES (?, ?, ?)",
            (symbol, quantity, buy_price)
        )

        imported += 1

    conn.commit()
    conn.close()

    print(f"Successfully imported {imported} stocks into portfolio!")

# Run directly
if __name__ == "__main__":
    import_portfolio_from_excel("portfolio.xlsx")