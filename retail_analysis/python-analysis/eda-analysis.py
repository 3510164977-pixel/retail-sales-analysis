import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')

df = pd.read_csv("/Users/lina/Downloads/demand_forecasting.csv")
df['Date'] = pd.to_datetime(df['Date'])

#Basic amounts
print(f"Time span: {df['Date'].min()} ~ {df['Date'].max()}")
print(f"Number of stores: {df['Store ID'].nunique()}")
print(f"Number of products: {df['Product ID'].nunique()}")
print(f"Number of categories {df['Category'].nunique()}")
print(f"Number of regions: {df['Region'].nunique()}")

#Distribution of numerical variables
numeric_cols = ['Inventory Level', 'Units Sold', 'Price', 'Discount',
                'Competitor Pricing', 'Demand']
print(df[numeric_cols].describe())

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Numerical variables', fontsize=16, fontweight='bold')
for i, col in enumerate(numeric_cols):
    row = i // 3
    col_idx = i % 3
    axes[row, col_idx].hist(df[col], bins=30, color='#1f77b4', alpha=0.7)
    axes[row, col_idx].set_title(f'{col} distribution')
    axes[row, col_idx].set_xlabel(col)
    axes[row, col_idx].set_ylabel('frequency')
plt.tight_layout()
plt.savefig('distribution_of_numerical_variables.png', dpi=300)
plt.close()
##Inventory levels are most frequent in 0-500, while sales: 50-100, demands: 70-130,
# the pricing of competitive products is similar with the own products. most discounts focus on 0, 5 and 10%.

plt.figure(figsize=(12, 6))
sns.boxplot(data=df[numeric_cols], palette='Set2')
plt.title('boxplot', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('boxplot_of_numerical_variables.png', dpi=300)
plt.close()
##The boxplot shows that there are some abnormal values in the inventory level,
# indicating that the inventory level of most stores is normal, but a few stores have a serious inventory backlog.
# Besides, the retail shop doesn't usually offer discounts .

#Distribution of categories
print("Categories")
print(df['Category'].value_counts())

print("\nNumber of regions：")
print(df['Region'].value_counts())
cat_cols = ['Seasonality', 'Weather Condition', 'Promotion', 'Epidemic']
for col in cat_cols:
    print(f"\n{col} distribution：")
    print(df[col].value_counts())
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Correlation analysis
print("Correlation matrix")
corr = df[numeric_cols].corr()
print(corr['Demand'].sort_values(ascending=False))

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Heat map of numerical variable correlation', fontsize=14)
plt.tight_layout()
plt.savefig('Heat map of correlation.png', dpi=300)
plt.close()
##Price is highly relative with competitive pricing.
# There is a strong positive correlation between demand and sales at 0.83, which is the core driving factor of demand.
# Discounts and inventory level only have a slight effect on demand.

#Time analysis
df['YearMonth'] = df['Date'].dt.to_period('M')
monthly_demand = df.groupby('YearMonth')['Demand'].sum().reset_index()
monthly_demand['YearMonth'] = monthly_demand['YearMonth'].astype(str)
plt.figure(figsize=(16, 6))
plt.plot(monthly_demand['YearMonth'], monthly_demand['Demand'], marker='o', linewidth=2, color='#d62728')
plt.title('Monthly demands', fontsize=14)
plt.xlabel('month')
plt.ylabel('total demands')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Monthly_demands.png', dpi=300)
plt.close()
##Summer is the peak of demand, and February is the low.

# Influence of business factors
promo_demand = df.groupby('Promotion')['Demand'].mean()
epidemic_demand = df.groupby('Epidemic')['Demand'].mean()
season_demand = df.groupby('Seasonality')['Demand'].mean().sort_values(ascending=False)
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
promo_demand.plot.bar(ax=axes[0], color=['#1f77b4','#ff7f0e'], title='Influence of promotion')
epidemic_demand.plot.bar(ax=axes[1], color=['#2ca02c','#d62728'], title='Influence of epidemic')
season_demand.plot.bar(ax=axes[2], title='Influence of seasons')
for ax in axes:
    ax.set_ylabel('Average demands')
    ax.tick_params(axis='x', rotation=0)
plt.subplots_adjust(wspace=0.5)
plt.savefig('Influence of business factors.png', dpi=300)
plt.show()
plt.close()
##Promotions can increase demand by 30%, and the epidemic has led to a 36% decline in demand.
# Summer is the peak season of demand, and spring is the off-season.