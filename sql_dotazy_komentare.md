# SQL Dotazy s komentářem

Tento dokument obsahuje všechny důležité SQL dotazy použití při zápočtovém projektu, doplněné stručným komentářem.

---

## 1. Celkové tržby podle roku

```sql
SELECT 
    d.Year,
    SUM(f.Revenue) AS TotalRevenue
FROM FactSales f
JOIN DimDate d ON f.DateID = d.DateID
GROUP BY d.Year
ORDER BY d.Year;
```

📝 *Vrací součet tržeb (Revenue) seskupený podle kalendářního roku.*

---

## 2. TOP 5 produktů podle zisku

```sql
SELECT 
    p.Product,
    SUM(f.Profit) AS TotalProfit
FROM FactSales f
JOIN DimProduct p ON f.ProductID = p.ProductID
GROUP BY p.Product
ORDER BY TotalProfit DESC
OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY;
```

📝 *Vrací pět produktů s nejvyšším celkovým ziskem.*

---

## 3. Podíl ekologických vs. neekologických produktů

```sql
SELECT 
    Eco_Friendly,
    COUNT(*) AS NumberOfOrders,
    SUM(Revenue) AS TotalRevenue
FROM FactSales
GROUP BY Eco_Friendly;
```

📝 *Porovnává počet a součet tržeb objednávek mezi ekologickými (`Eco_Friendly = 1`) a neekologickými (`Eco_Friendly = 0`) produkty.*

---

## 4. Průměrný zisk podle věkové skupiny zákazníků

```sql
SELECT 
    c.Age_Group,
    AVG(f.Profit) AS AverageProfit
FROM FactSales f
JOIN DimCustomer c ON f.CustomerID = c.CustomerID
GROUP BY c.Age_Group
ORDER BY AverageProfit DESC;
```

📝 *Ukazuje, které věkové skupiny zákazníků generují nejvyšší průměrný zisk.*

---

## 5. Pokročilý dotaz – Segmentace zákazníků podle průměrné hodnoty objednávky

```sql
WITH CustomerAverages AS (
    SELECT 
        c.CustomerID,
        c.Age_Group,
        c.Country,
        COUNT(f.FactID) AS OrderCount,
        SUM(f.Revenue) AS TotalRevenue,
        AVG(f.Revenue) AS AvgOrderValue
    FROM FactSales f
    JOIN DimCustomer c ON f.CustomerID = c.CustomerID
    GROUP BY c.CustomerID, c.Age_Group, c.Country
),
CustomerSegments AS (
    SELECT *,
        CASE 
            WHEN AvgOrderValue > 1000 THEN 'High-Value'
            WHEN AvgOrderValue BETWEEN 500 AND 1000 THEN 'Mid-Value'
            ELSE 'Low-Value'
        END AS Segment
    FROM CustomerAverages
)
SELECT 
    Segment,
    COUNT(*) AS NumberOfCustomers,
    AVG(AvgOrderValue) AS SegmentAvgOrder,
    SUM(TotalRevenue) AS SegmentRevenue
FROM CustomerSegments
GROUP BY Segment
ORDER BY SegmentAvgOrder DESC;
```

📝 *Rozděluje zákazníky do tří segmentů podle hodnoty průměrné objednávky a zobrazuje souhrnné statistiky pro každý segment.*

