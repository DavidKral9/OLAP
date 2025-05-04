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
WITH CustomerAverages AS (
    SELECT 
        c.CustomerID,
        AVG(f.Revenue) AS AvgOrderValue
    FROM FactSales f
    JOIN DimCustomer c ON f.CustomerID = c.CustomerID
    GROUP BY c.CustomerID
),
CustomerSegments AS (
    SELECT 
        CASE 
            WHEN AvgOrderValue > 1000 THEN 'High-Value'
            WHEN AvgOrderValue BETWEEN 500 AND 1000 THEN 'Mid-Value'
            ELSE 'Low-Value'
        END AS Segment
    FROM CustomerAverages
)
SELECT Segment, COUNT(*) AS PocetZakazniku
FROM CustomerSegments
GROUP BY Segment;
"""
df = pd.read_sql_query(query, conn)
plt.figure(figsize=(6, 6))
plt.pie(df['PocetZakazniku'], labels=df['Segment'], autopct='%1.1f%%', startangle=140)
plt.title("Segmentace zákazníků podle průměrné hodnoty objednávky")
plt.tight_layout()
plt.show()