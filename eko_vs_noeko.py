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
SELECT 
    CASE WHEN Eco_Friendly = 1 THEN 'Ekologické' ELSE 'Neekologické' END AS Typ,
    COUNT(*) AS Pocet,
    SUM(Revenue) AS Trzby
FROM FactSales
GROUP BY Eco_Friendly;
"""
df = pd.read_sql(query, conn)
plt.figure(figsize=(6, 6))
plt.pie(df['Trzby'], labels=df['Typ'], autopct='%1.1f%%', startangle=140, colors=['green', 'gray'])
plt.title("Podíl tržeb ekologických a neekologických produktů")
plt.tight_layout()
plt.show()