Retail demand forecasting using Pandas, MySQL and visualization tools.
This project conducts business analysis based on product demand forecasting data. The entire workflow includes Pandas data cleaning， feature engineering, MySQL analysis, Pandas exploratory analysis and visualization with Matplotlib, Seaborn and Tableau.
The analysis explores core business factors including product category, regional distribution, promotion, epidemic impact, seasonal fluctuation, inventory health and monthly demand year-on-year growth, providing data-driven insights for inventory management, marketing strategies and operational optimization.
# Environment 
Python 3.8+
MySQL 8.0+
Tableau Public (Web Version, MacOS adapted)
MacOS Operating System
# Required Python Libraries
pandas
matplotlib
seaborn
sqlalchemy
mysql-connector-python
# Installation Command
pip install pandas matplotlib seaborn sqlalchemy mysql-connector-python
       
# Workflow
1. Data Preprocessing (data/demand_preprocessing.py)

Convert raw date strings to standard datetime format
Extract time features: Year, Month, Day, DayOfWeek
Create business indicators: Revenue, Discount_Rate, Inventory_Ratio, Price_Competitive
Export standardized cleaned data for MySQL import and subsequent analysis

2. MySQL Data Import (sql/MySQL.py)

Connect to local MySQL database, create the target database, and import the processed data for SQL analysis.

3. Analysis using MySQL (My_sql_operation/)

All SQL analysis scripts and results are stored in My_sql_operation/, covering core business dimensions:
Basic dataset overview & table structure check
Category-wise total/average demand analysis
Regional demand distribution ranking
Promotion impact on average demand
Joint impact of seasonality and epidemic
Store inventory health assessment (inventory-demand ratio)
Price comparison between own products and competitors
Demand performance under different discount levels
Top 5 stores by total demand
Top 3 demand categories per region
Top 5 high-inventory products per store
Core metric: Monthly demand YoY growth rate calculation
Inventory status classification (excess/normal/shortage)
Seasonal demand fluctuation analysis by category

4. Python EDA & Visualization (python-analysis/eda-analysis.py)

Generate high-resolution statistical charts to explore data distribution, correlations, trends, and business factors:
Numerical variable distribution histograms
Boxplots for outlier detection (inventory overstock/extreme values)
Correlation heatmap of key business indicators
Monthly total demand time series trend
Bar charts for demand impact factors (promotion, epidemic, seasonality)
All visualization outputs are saved in the python-analysis/ folder.

5. Tableau Interactive Visualization (MacOS Web Version)

# Key Analysis Findings
Summer is the peak demand season, while February records the lowest monthly demand.
Promotions increase average demand by ~30%; the epidemic caused a significant 36% drop in overall demand.
Most stores maintain normal inventory levels, while a small number face severe inventory overstock.
Demand has a strong positive correlation (0.83) with unit sales; discount and inventory level have limited impact on demand.
Own product pricing is highly consistent with competitor pricing across all categories.
Most merchants adopt zero or low-discount strategies in daily operations.

# License
This project is for academic learning, business analysis practice, and portfolio use only.
