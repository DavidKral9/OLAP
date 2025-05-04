import pandas as pd
import pyodbc
import os


csv_filename = 'bike_sales.csv'  

# Název tabulky = název souboru bez přípony
table_name = os.path.splitext(csv_filename)[0]

# Připojení k databázi pomocí Windows autentizace
server = 'LAPTOP-UIDJILKD'  
database = 'BikeSales'      
conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)

# Cesta k CSV souboru
file_path = os.path.join(os.path.dirname(__file__), csv_filename)

# Načti CSV – se středníky a UTF-8
df = pd.read_csv(file_path, sep=';', encoding='utf-8')

#  Připojení
with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()

    # Vytvoření tabulky, pokud ještě neexistuje
    columns = ', '.join([f"[{col}] NVARCHAR(MAX)" for col in df.columns])
    if_not_exists = f"IF OBJECT_ID('{table_name}', 'U') IS NULL "
    create_query = f"CREATE TABLE {table_name} ({columns})"
    cursor.execute(if_not_exists + create_query)
    conn.commit()

    #  Vkládání dat
    for index, row in df.iterrows():
        placeholders = ', '.join(['?' for _ in row])
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        try:
            cursor.execute(insert_query, tuple(row.astype(str)))
        except Exception as e:
            print(f"Chyba na řádku {index + 2}: {e}")
    conn.commit()

print(f"✅ Hotovo – data ze souboru '{csv_filename}' byla vložena do tabulky '{table_name}'.")
