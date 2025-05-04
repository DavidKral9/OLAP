import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# Připojení k databázi (úprava podle tvého prostředí)
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=LAPTOP-UIDJILKD;'
    'DATABASE=BikeSales;'
    'Trusted_Connection=yes;'
)
query = """
SELECT TOP 5 p.Product, SUM(f.Profit) AS TotalProfit
FROM FactSales f
JOIN DimProduct p ON f.ProductID = p.ProductID
GROUP BY p.Product
ORDER BY TotalProfit DESC;
"""
df = pd.read_sql_query(query, conn)
plt.figure(figsize=(10, 5))
plt.barh(df['Product'], df['TotalProfit'], color='orange')
plt.title("TOP 5 produktů podle zisku")
plt.xlabel("Celkový zisk (Kč)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()