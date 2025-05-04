import pandas as pd
import pyodbc
import matplotlib.pyplot as plt

# Připojení k databázi
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=LAPTOP-UIDJILKD;'
    'DATABASE=BikeSales;'
    'Trusted_Connection=yes;'
)

# SQL dotaz
query = """
SELECT 
    c.Age_Group,
    AVG(f.Profit) AS AverageProfit
FROM FactSales f
JOIN DimCustomer c ON f.CustomerID = c.CustomerID
GROUP BY c.Age_Group
ORDER BY AverageProfit DESC;
"""

# Načtení dat
df = pd.read_sql(query, conn)

# Vykreslení grafu
plt.figure(figsize=(8, 5))
plt.bar(df['Age_Group'], df['AverageProfit'], color='purple')
plt.title("Průměrný zisk podle věkové skupiny")
plt.xlabel("Věková skupina")
plt.ylabel("Průměrný zisk (Kč)")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()