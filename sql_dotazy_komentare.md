# SQL Dotazy s komentářem

Tento dokument obsahuje všechny důležité SQL dotazy použití při zápočtovém projektu

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

📝 *Porovnává počet a součet tržeb objednávek mezi ekologickými a neekologickými produkty.*

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

---

## 📦 Vytvoření tabulek dimenzí a faktové tabulky

### DimDate

```sql
CREATE TABLE DimDate (
    DateID INT IDENTITY(1,1) PRIMARY KEY,
    [Date] DATE,
    Day INT,
    MonthName NVARCHAR(20),
    Year INT
);
```
-- Naplnění DimDate
```sql
INSERT INTO DimDate ([Date], Day, MonthName, Year)
SELECT DISTINCT [Date], [Day], [Month], [Year]
FROM bike_sales_with_id;
```
### DimCustomer

```sql
CREATE TABLE DimCustomer (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    Customer_Age INT,
    Age_Group NVARCHAR(50),
    Customer_Gender NVARCHAR(20),
    Country NVARCHAR(50),
    State NVARCHAR(50)
);
```
-- Naplnění DimCustomer
```sql
INSERT INTO DimCustomer (Customer_Age, Age_Group, Customer_Gender, Country, State)
SELECT DISTINCT Customer_Age, Age_Group, Customer_Gender, Country, State
FROM bike_sales_with_id;
```

### DimProduct

```sql
CREATE TABLE DimProduct (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    Product NVARCHAR(100),
    Sub_Category NVARCHAR(100),
    Product_Category NVARCHAR(100),
    Manufacturer NVARCHAR(100),
    Color NVARCHAR(50),
    Size NVARCHAR(50),
    Material NVARCHAR(50),
    Warranty NVARCHAR(50)
);
```
-- Naplnění DimProduct
```sql
INSERT INTO DimProduct (Product, Sub_Category, Product_Category, Manufacturer, Color, Size, Material, Warranty)
SELECT DISTINCT Product, Sub_Category, Product_Category, Manufacturer, Color, Size, Material, Warranty
FROM bike_sales_with_id;
```

### FactSales

```sql
CREATE TABLE FactSales (
    FactID INT IDENTITY(1,1) PRIMARY KEY,
    DateID INT,
    CustomerID INT,
    ProductID INT,
    Order_Quantity INT,
    Unit_Cost FLOAT,
    Unit_Price FLOAT,
    Profit FLOAT,
    Cost FLOAT,
    Revenue FLOAT,
    Discount FLOAT,
    Eco_Friendly BIT,
    Shipping_Cost FLOAT,
    Delivery_Time INT,
    Rating INT,
    FOREIGN KEY (DateID) REFERENCES DimDate(DateID),
    FOREIGN KEY (CustomerID) REFERENCES DimCustomer(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES DimProduct(ProductID)
);
```
-- INSERT INTO FactSales pomocí JOIN
```sql
INSERT INTO FactSales (
    DateID, CustomerID, ProductID,
    Order_Quantity, Unit_Cost, Unit_Price,
    Profit, Cost, Revenue, Discount,
    Eco_Friendly, Shipping_Cost, Delivery_Time, Rating
)
SELECT
    d.DateID, c.CustomerID, p.ProductID,
    s.Order_Quantity, s.Unit_Cost, s.Unit_Price,
    s.Profit, s.Cost, s.Revenue, s.Discount,
    s.Eco_Friendly, s.Shipping_Cost, s.Delivery_Time, s.Rating
FROM bike_sales_with_id s
JOIN DimDate d ON s.[Date] = d.[Date] AND s.[Day] = d.Day AND s.[Month] = d.MonthName AND s.[Year] = d.Year
JOIN DimCustomer c ON s.Customer_Age = c.Customer_Age AND s.Age_Group = c.Age_Group AND s.Customer_Gender = c.Customer_Gender AND s.Country = c.Country AND s.State = c.State
JOIN DimProduct p ON s.Product = p.Product AND s.Sub_Category = p.Sub_Category AND s.Product_Category = p.Product_Category AND s.Manufacturer = p.Manufacturer AND s.Color = p.Color AND s.Size = p.Size AND s.Material = p.Material AND s.Warranty = p.Warranty;
```


