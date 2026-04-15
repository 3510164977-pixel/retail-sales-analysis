CREATE DATABASE IF NOT EXISTS demand_db;
USE demand_db;

SELECT COUNT(*) FROM demand_data;
DESCRIBE demand_data;

-- Total demand and average demand of each category
SELECT category, SUM(demand) AS total_demand, AVG(demand) AS avg_demand
FROM demand_data GROUP BY category ORDER BY total_demand DESC;

-- Demands of each region
SELECT region, SUM(demand) AS total_demand
FROM demand_data GROUP BY region ORDER BY total_demand DESC;

-- The impact of promotion on demand
SELECT CASE WHEN promotion=1 THEN 'has promotion' ELSE 'no promotion' END AS promotion_status,
AVG(demand) AS avg_demand FROM demand_data GROUP BY promotion;

-- The impact of season and epidemic on demand
SELECT seasonality, CASE WHEN epidemic=1 THEN '疫情期' ELSE '正常' END AS status,
AVG(demand) AS avg_demand FROM demand_data GROUP BY seasonality, epidemic;

-- The stores which inventory level/Demand>3
SELECT `store id`, AVG(`inventory level`) AS avg_inventory, AVG(demand) AS avg_demand,
AVG(`inventory level`/(demand+1)) AS inventory_ratio
FROM demand_data GROUP BY `store id` HAVING inventory_ratio>3 ORDER BY inventory_ratio DESC;

-- Comparison between prices and competitor prices
SELECT category, AVG(price) AS avg_price, AVG(`competitor pricing`) AS competitor_price
FROM demand_data GROUP BY category;

-- The impact of discount on demand
SELECT 
    discount, AVG(demand) AS avg_demand
FROM
    demand_data
GROUP BY discount
ORDER BY discount;

-- TOP 5 stores with the highest demand
WITH store_rank AS (
    SELECT `store id`, SUM(demand) AS total_demand,
    RANK() OVER(ORDER BY SUM(demand) DESC) AS rnk FROM demand_data GROUP BY `store id`
)
SELECT `store id`, total_demand FROM store_rank WHERE rnk<=5;

-- TOP 3 categories with the highest demand in each region
WITH category_rank AS (
    SELECT
        Region,
        Category,
        SUM(Demand) AS total_demand,
        RANK() OVER(PARTITION BY Region ORDER BY SUM(Demand) DESC) AS rnk
    FROM demand_data
    GROUP BY Region, Category
)
SELECT * FROM category_rank WHERE rnk <= 3;

-- TOP 5 products with the highest inventory in each store
WITH product_inventory AS (
    SELECT
        `Store ID`,
        `Product ID`,
        Category,
        AVG(`Inventory Level`) AS avg_inventory,
        ROW_NUMBER() OVER(PARTITION BY `Store ID` ORDER BY AVG(`Inventory Level`) DESC) AS rnk
    FROM demand_data
    GROUP BY `Store ID`, `Product ID`, Category
)
SELECT * FROM product_inventory WHERE rnk <=5;

-- Growth rate of monthly demand this year vs last year
WITH monthly_data AS (
    SELECT
        YEAR(`date`) AS year,
        MONTH(`date`) AS month,
        SUM(Demand) AS total_demand
    FROM demand_data
    GROUP BY YEAR(`date`),MONTH(`date`)
)
SELECT
    curr.year,
    curr.month,
    curr.total_demand AS current_demand,
    prev.total_demand AS last_year_demand,
    ROUND((curr.total_demand - prev.total_demand)/prev.total_demand *100, 2) AS yoy_growth_rate
FROM monthly_data curr
LEFT JOIN monthly_data prev ON curr.month = prev.month AND curr.year = prev.year+1
ORDER BY curr.year, curr.month;

-- Categories with the highest demand under the pandemic and non-epidemic
WITH epidemic_category AS (
    SELECT
        CASE WHEN Epidemic=1 THEN 'Epidemic' ELSE 'No epidemic' END AS epidemic_status,
        Category,
        Epidemic,
        SUM(Demand) AS total_demand,
        DENSE_RANK() OVER(PARTITION BY Epidemic ORDER BY SUM(Demand) DESC) AS rnk
    FROM demand_data
    GROUP BY epidemic_status, Category, Epidemic
)
SELECT * FROM epidemic_category WHERE rnk =1;

-- Stores with excess/normal/shortage inventory
SELECT
    `Store ID`,
    Region,
    AVG(`Inventory Level`) AS avg_inventory,
    AVG(Demand) AS avg_demand,
    CASE
        WHEN AVG(`Inventory Level`) > AVG(Demand)*3 THEN 'Excess inventory'
        WHEN AVG(`Inventory Level`) < AVG(Demand)*0.5 THEN 'Inventory with shortage'
        ELSE 'Normal inventory'
    END AS inventory_status
FROM demand_data
GROUP BY `Store ID`, Region;

-- The category with the largest demand fluctuations in each season
WITH season_stats AS (
    SELECT
        Seasonality,
        Category,
        STDDEV(Demand) AS demand_std, 
        RANK() OVER(PARTITION BY Seasonality ORDER BY STDDEV(Demand) DESC) AS rnk
    FROM demand_data
    GROUP BY Seasonality, Category
)
SELECT * FROM season_stats WHERE rnk <=3;

