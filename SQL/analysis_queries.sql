-- Ecommerce Sales Analysis Project
-- Author: Vidit Bhatnagar
-- Description: SQL queries for revenue, customer, and product insights

CREATE DATABASE ecommerce_project;
USE ecommerce_project;
CREATE TABLE ecommerce_data (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description TEXT,
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice FLOAT,
    CustomerID FLOAT,
    Country VARCHAR(50),
    TotalPrice FLOAT
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_data.csv'
INTO TABLE ecommerce_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

USE ecommerce_project;

-- KPI METRICS
-- Total Revenue
SELECT ROUND(SUM(TotalPrice), 2) AS Total_Revenue
FROM ecommerce_data;

-- Total Orders
SELECT COUNT(DISTINCT InvoiceNo) AS Total_Orders
FROM ecommerce_data;

-- Total Customers
SELECT COUNT(DISTINCT CustomerID) AS Total_Customers
FROM ecommerce_data;

-- Average Order Value
SELECT 
    ROUND(SUM(TotalPrice) / COUNT(DISTINCT InvoiceNo), 2) AS Avg_Order_Value
FROM ecommerce_data;

-- Monthly Revenue Trend
SELECT 
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS Month,
    ROUND(SUM(TotalPrice), 2) AS Revenue
FROM ecommerce_data
GROUP BY Month
ORDER BY Month;

-- Daily Revenue Trend
SELECT 
    DATE(InvoiceDate) AS Date,
    ROUND(SUM(TotalPrice), 2) AS Revenue
FROM ecommerce_data
GROUP BY Date
ORDER BY Date;

-- Top 10 Products by Revenue
SELECT 
    Description,
    ROUND(SUM(TotalPrice), 2) AS Revenue
FROM ecommerce_data
GROUP BY Description
ORDER BY Revenue DESC
LIMIT 10;

-- Top 10 Products by Quantity Sold
SELECT 
    Description,
    SUM(Quantity) AS Total_Quantity
FROM ecommerce_data
GROUP BY Description
ORDER BY Total_Quantity DESC
LIMIT 10;

-- Top 10 Customers by Spending
SELECT 
    CustomerID,
    ROUND(SUM(TotalPrice), 2) AS Total_Spent
FROM ecommerce_data
GROUP BY CustomerID
ORDER BY Total_Spent DESC
LIMIT 10;

-- Repeat Customers (More than 1 order)
SELECT 
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS Orders
FROM ecommerce_data
GROUP BY CustomerID
HAVING Orders > 1
ORDER BY Orders DESC;

-- Revenue by Country
SELECT 
    Country,
    ROUND(SUM(TotalPrice), 2) AS Revenue
FROM ecommerce_data
GROUP BY Country
ORDER BY Revenue DESC;

-- Top 5 Countries by Customers
SELECT 
    Country,
    COUNT(DISTINCT CustomerID) AS Customers
FROM ecommerce_data
GROUP BY Country
ORDER BY Customers DESC
LIMIT 5;

-- Customer Lifetime Value (CLV)
SELECT 
    CustomerID,
    ROUND(SUM(TotalPrice), 2) AS Lifetime_Value
FROM ecommerce_data
GROUP BY CustomerID
ORDER BY Lifetime_Value DESC;

-- Orders per Customer
SELECT 
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS Total_Orders
FROM ecommerce_data
GROUP BY CustomerID
ORDER BY Total_Orders DESC;

-- Average Revenue per Customer
SELECT 
    ROUND(SUM(TotalPrice) / COUNT(DISTINCT CustomerID), 2) AS Avg_Revenue_Per_Customer
FROM ecommerce_data;