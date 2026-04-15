import pandas as pd

df = pd.read_csv("/Users/lina/Downloads/demand_forecasting.csv",encoding_errors="ignore")
print(df.head())
print(df.shape)
print(df.describe())
print(df.duplicated().sum())
print(df.isnull().sum())
print(df.dtypes)

df["Date"] = pd.to_datetime(df["Date"])
df = df[df['Demand'] >= 0]
df = df[df['Inventory Level'] >= 0]

#Time characteristics
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['DayOfWeek'] = df['Date'].dt.dayofweek

#Indicators
df['Revenue'] = df['Price'] * df['Units Sold']
df['Discount_Rate'] = df['Discount'] / 100
df['Inventory_Ratio'] = df['Inventory Level'] / (df['Demand'] + 1)
df['Price_Competitive'] = df['Price'] / df['Competitor Pricing']

df.to_csv("/Users/lina/Downloads/demand_forecasting.csv",index=False)