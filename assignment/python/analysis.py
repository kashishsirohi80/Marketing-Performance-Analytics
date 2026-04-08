import pandas as pd
import sqlite3

# ===============================
# SHOPIFY DATA CLEANING
# ===============================

df = pd.read_csv("data/Raw_Shopify_Sales.csv")

# Remove duplicates
df = df.drop_duplicates()

# Date conversion
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Order Created At'] = pd.to_datetime(df['Order Created At'], errors='coerce')

# Remove invalid dates
df = df.dropna(subset=['Date'])

# Numerical cleaning
num_cols = [
    'Gross Sales (INR)', 'Net Sales (INR)', 'Total Sales (INR)',
    'Orders', 'Items Sold', 'Items Returned',
    'Discounts (INR)', 'Returns (INR)'
]

for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].median())

# String cleaning
str_cols = [
    'Shipping Country', 'Billing Country',
    'Customer Sale Type', 'Product Type'
]

for col in str_cols:
    if col in df.columns:
        df[col] = df[col].fillna("unknown")
        df[col] = df[col].str.lower().str.strip()

# Remove invalid values
df = df[df['Total Sales (INR)'] >= 0]
df = df[df['Orders'] >= 0]

# Derived metrics
df['return_rate'] = df['Items Returned'] / df['Items Sold']
df['aov'] = df['Total Sales (INR)'] / df['Orders']
df = df.replace([float('inf'), -float('inf')], 0)

print("Shopify cleaned ✅")


# ===============================
# CAMPAIGN DATA CLEANING
# ===============================

df_campaign = pd.read_csv("data/Campaign_Raw.csv", delimiter=",", engine="python")

df_campaign['Date'] = pd.to_datetime(df_campaign['Date'], errors='coerce')
df_campaign = df_campaign.dropna(subset=['Date'])

df_campaign.rename(columns={
    'Clicks (all)': 'clicks',
    'Impressions': 'impressions',
    'Amount Spent (INR)': 'spend',
    'Purchases': 'purchases',
    'Purchases Conversion Value (INR)': 'revenue'
}, inplace=True)

num_cols = ['clicks', 'impressions', 'spend', 'purchases', 'revenue']

for col in num_cols:
    df_campaign[col] = pd.to_numeric(df_campaign[col], errors='coerce')

# 🔥 FIX NaN
df_campaign['Campaign Name'] = df_campaign['Campaign Name'].fillna("unknown_campaign")
df_campaign['Country Funnel'] = df_campaign['Country Funnel'].fillna("unknown_country")

# Only fill specific columns
df_campaign['Campaign Name'] = df_campaign['Campaign Name'].fillna("unknown_campaign")
df_campaign['Country Funnel'] = df_campaign['Country Funnel'].fillna("unknown_country")

# Numeric columns safe fill
for col in ['clicks', 'impressions', 'spend', 'purchases', 'revenue']:
    df_campaign[col] = df_campaign[col].fillna(0)

# Metrics (SAFE)
df_campaign['CTR'] = df_campaign['clicks'] / df_campaign['impressions']

df_campaign['CPC'] = df_campaign.apply(
    lambda x: x['spend'] / x['clicks'] if x['clicks'] > 0 else 0,
    axis=1
)

df_campaign['CPM'] = df_campaign.apply(
    lambda x: (x['spend'] / x['impressions']) * 1000 if x['impressions'] > 0 else 0,
    axis=1
)

df_campaign['ROI'] = df_campaign.apply(
    lambda x: (x['revenue'] - x['spend']) / x['spend'] if x['spend'] > 0 else 0,
    axis=1
)

df_campaign = df_campaign.replace([float('inf'), -float('inf')], 0)

# Normalize text
df_campaign['Campaign Name'] = df_campaign['Campaign Name'].str.lower().str.strip()
df_campaign['Country Funnel'] = df_campaign['Country Funnel'].str.lower().str.strip()

print("Campaign cleaned properly ✅")


# ===============================
# CONNECT FINAL DB
# ===============================

conn = sqlite3.connect("final.db")


# ===============================
# INSERT FACT SALES
# ===============================

fact_sales = df[[
    'Order ID', 'Date', 'Product ID', 'Product Type', 'Shipping Country',
    'Total Sales (INR)', 'Net Sales (INR)', 'Gross Sales (INR)',
    'Orders', 'Items Sold', 'Items Returned'
]].copy()

fact_sales['return_rate'] = fact_sales['Items Returned'] / fact_sales['Items Sold']
fact_sales['aov'] = fact_sales['Total Sales (INR)'] / fact_sales['Orders']

fact_sales = fact_sales.replace([float('inf'), -float('inf')], 0)

fact_sales.columns = [
    'order_id', 'date', 'product_id', 'product_type', 'shipping_country',
    'total_sales', 'net_sales', 'gross_sales',
    'orders', 'items_sold', 'items_returned',
    'return_rate', 'aov'
]

fact_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)

print("fact_sales inserted ✅")


# ===============================
# INSERT FACT CAMPAIGN
# ===============================

fact_campaign = df_campaign[[
    'Campaign Name', 'Date', 'Country Funnel',
    'impressions', 'clicks', 'spend',
    'purchases', 'revenue',
    'CTR', 'CPC', 'CPM', 'ROI'
]].copy()

fact_campaign.columns = [
    'campaign_name', 'date', 'country',
    'impressions', 'clicks', 'spend',
    'purchases', 'revenue',
    'CTR', 'CPC', 'CPM', 'ROI'
]

fact_campaign.to_sql("fact_campaign", conn, if_exists="replace", index=False)

print("fact_campaign inserted ✅")


# ===============================
# DATE DIMENSION
# ===============================

date_dim = pd.DataFrame()

date_dim['date'] = pd.to_datetime(df['Date']).dropna().unique()
date_dim['date'] = pd.to_datetime(date_dim['date'])

date_dim['year'] = date_dim['date'].dt.year
date_dim['month'] = date_dim['date'].dt.month
date_dim['day'] = date_dim['date'].dt.day
date_dim['quarter'] = date_dim['date'].dt.quarter

date_dim.to_sql("date_dim", conn, if_exists="replace", index=False)

print("date_dim inserted ✅")


# ===============================
# FINAL CHECK
# ===============================

print(pd.read_sql("SELECT * FROM fact_sales LIMIT 5", conn))
print(pd.read_sql("SELECT * FROM fact_campaign LIMIT 5", conn))
conn = sqlite3.connect("final.db")

print(pd.read_sql("SELECT COUNT(*) FROM fact_sales", conn))
print(pd.read_sql("SELECT COUNT(*) FROM fact_campaign", conn))
conn = sqlite3.connect("final.db")

pd.read_sql("SELECT * FROM fact_sales", conn).to_csv("fact_sales.csv", index=False)
pd.read_sql("SELECT * FROM fact_campaign", conn).to_csv("fact_campaign.csv", index=False)
pd.read_sql("SELECT * FROM date_dim", conn).to_csv("date_dim.csv", index=False)

conn.close()

conn.close()

conn.close()

print("ALL DATA INSERTED SUCCESSFULLY 🔥")