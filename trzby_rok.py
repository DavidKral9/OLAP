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

# SQL dotaz
query = """
SELECT d.Year, SUM(f.Revenue) AS TotalRevenue
FROM FactSales f
JOIN DimDate d ON f.DateID = d.DateID
GROUP BY d.Year
ORDER BY d.Year;
"""

# Načtení výsledků do DataFrame
df = pd.read_sql(query, conn)

# Graf
plt.figure(figsize=(8, 5))
plt.bar(df['Year'], df['TotalRevenue'], color='steelblue')
plt.title("Celkové tržby podle roku")
plt.xlabel("Rok")
plt.ylabel("Tržby")
plt.grid(True)
plt.tight_layout()
plt.show()