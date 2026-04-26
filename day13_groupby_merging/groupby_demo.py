# ============================================================
# DAY 13 — PANDAS GroupBy: Complete Sales Data Analysis
# ============================================================
# Dataset: Synthetic "TechMart Sales" data (created inline)
# Topics covered:
#   - groupby basics (single col, multiple cols)
#   - built-in aggregations (sum, mean, min, max, count, std)
#   - GroupBy attributes (len, size, first/last/nth, get_group,
#                         groups, describe, sample, nunique)
#   - agg() method (dict, list, named aggregations)
#   - apply() on groups (custom func, ranking, normalization)
#   - looping over groups
# ============================================================

import pandas as pd
import numpy as np

np.random.seed(42)

# ── Build a realistic Sales Dataset ─────────────────────────
n = 200
regions    = ['North', 'South', 'East', 'West']
categories = ['Electronics', 'Clothing', 'Groceries', 'Books', 'Sports']
products   = {
    'Electronics': ['Laptop', 'Phone', 'Tablet', 'Headphones'],
    'Clothing':    ['Jacket', 'Shoes', 'T-Shirt', 'Jeans'],
    'Groceries':   ['Rice', 'Oil', 'Sugar', 'Pasta'],
    'Books':       ['Fiction', 'Science', 'History', 'Comics'],
    'Sports':      ['Bat', 'Ball', 'Gloves', 'Racket'],
}

category_col = np.random.choice(categories, n)
product_col  = [np.random.choice(products[c]) for c in category_col]
region_col   = np.random.choice(regions, n)
price_map    = {'Electronics': (200, 1500), 'Clothing': (20, 300),
                'Groceries': (5, 50), 'Books': (10, 60), 'Sports': (15, 200)}
units_col    = np.random.randint(1, 20, n)
price_col    = np.array([round(np.random.uniform(*price_map[c]), 2) for c in category_col])
revenue_col  = (units_col * price_col).round(2)
months       = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_col    = np.random.choice(months, n)
salesperson_col = np.random.choice(['Alice', 'Bob', 'Carol', 'Dave', 'Eve'], n)

df = pd.DataFrame({
    'Region':      region_col,
    'Category':    category_col,
    'Product':     product_col,
    'Month':       month_col,
    'Salesperson': salesperson_col,
    'Units':       units_col,
    'Price':       price_col,
    'Revenue':     revenue_col,
})

print("=" * 65)
print("  TECHMART SALES DATASET — Overview")
print("=" * 65)
print(f"Shape: {df.shape}  |  Columns: {df.columns.tolist()}")
print()
print(df.head(6).to_string())
print()

# ============================================================
print("=" * 65)
print("  SECTION 1: GROUPBY BASICS")
print("=" * 65)
# ── 1A. Single column groupby ────────────────────────────────
# groupby returns a GroupBy object — a set of groups
# You MUST follow with an aggregation to get a result

print("\n[1A] Total Revenue per Category (single col groupby + sum):")
cat_revenue = df.groupby('Category')['Revenue'].sum().round(2)
print(cat_revenue.sort_values(ascending=False))
# Output: Series indexed by Category

print("\n[1B] Average Unit Price per Region:")
region_avg = df.groupby('Region')['Price'].mean().round(2)
print(region_avg)

print("\n[1C] Multiple columns — sum of both Units AND Revenue per Category:")
multi_agg = df.groupby('Category')[['Units', 'Revenue']].sum()
print(multi_agg.sort_values('Revenue', ascending=False))

# ── 1D. Multiple groupby keys ────────────────────────────────
print("\n[1D] Revenue grouped by Region AND Category (2 keys):")
region_cat = df.groupby(['Region', 'Category'])['Revenue'].sum().round(2)
print(region_cat.head(12))
# Result: MultiIndex Series

print("\n[1E] Unstack MultiIndex to pivot table style:")
pivot_style = region_cat.unstack(fill_value=0)
print(pivot_style.round(0).to_string())

print()

# ============================================================
print("=" * 65)
print("  SECTION 2: GROUPBY ATTRIBUTES & METHODS")
print("=" * 65)

grp = df.groupby('Category')   # GroupBy object

# ── 2A. len ─────────────────────────────────────────────────
print(f"\n[2A] len(grp) — number of groups: {len(grp)}")

# ── 2B. size ────────────────────────────────────────────────
print("\n[2B] grp.size() — number of rows per group:")
print(grp.size())
# size() includes NaN rows | count() excludes NaN rows

# ── 2C. groups ──────────────────────────────────────────────
print("\n[2C] grp.groups — dict of {group_label: [index list]}")
for key, idx in grp.groups.items():
    print(f"   '{key}': {len(idx)} rows  →  first 5 indices: {list(idx[:5])}")

# ── 2D. get_group ────────────────────────────────────────────
print("\n[2D] grp.get_group('Electronics') — extract one group:")
electronics = grp.get_group('Electronics')
print(f"   Electronics group shape: {electronics.shape}")
print(electronics[['Product', 'Units', 'Revenue']].head(4).to_string())

# ── 2E. first / last / nth ───────────────────────────────────
print("\n[2E] grp.first() — first row of each group:")
print(grp[['Product', 'Revenue']].first())

print("\n[2F] grp.last() — last row of each group:")
print(grp[['Product', 'Revenue']].last())

print("\n[2G] grp.nth(2) — 3rd row (index 2) of each group:")
print(grp[['Product', 'Revenue']].nth(2))

# ── 2F. describe ─────────────────────────────────────────────
print("\n[2H] grp['Revenue'].describe() — stats per group:")
print(grp['Revenue'].describe().round(2))

# ── 2G. sample ───────────────────────────────────────────────
print("\n[2I] grp.sample(1, random_state=1) — 1 random row per group:")
print(grp[['Category', 'Product', 'Revenue']].sample(1, random_state=1).to_string())

# ── 2H. nunique ──────────────────────────────────────────────
print("\n[2J] grp['Product'].nunique() — unique products per category:")
print(grp['Product'].nunique())

print()

# ============================================================
print("=" * 65)
print("  SECTION 3: agg() METHOD")
print("=" * 65)
# agg() = apply MULTIPLE aggregations at once
# Three ways to call:

# ── 3A. List of functions (same for all selected columns) ────
print("\n[3A] agg(['sum','mean','max']) on Revenue per Category:")
result_3a = df.groupby('Category')['Revenue'].agg(['sum', 'mean', 'max']).round(2)
print(result_3a)

# ── 3B. Dict — different function per column ─────────────────
print("\n[3B] agg(dict) — different aggs per column:")
result_3b = df.groupby('Category').agg({
    'Revenue': ['sum', 'mean'],
    'Units':   ['sum', 'max'],
    'Price':   'mean',
})
result_3b.columns = ['Total_Revenue', 'Avg_Revenue', 'Total_Units', 'Max_Units', 'Avg_Price']
result_3b = result_3b.round(2)
print(result_3b.to_string())

# ── 3C. Named aggregations (cleanest — pandas 0.25+) ─────────
print("\n[3C] Named aggregations using pd.NamedAgg:")
result_3c = df.groupby('Region').agg(
    Total_Revenue  = pd.NamedAgg(column='Revenue', aggfunc='sum'),
    Avg_Revenue    = pd.NamedAgg(column='Revenue', aggfunc='mean'),
    Total_Units    = pd.NamedAgg(column='Units',   aggfunc='sum'),
    Unique_Products= pd.NamedAgg(column='Product', aggfunc='nunique'),
    Top_Sale       = pd.NamedAgg(column='Revenue', aggfunc='max'),
).round(2)
print(result_3c.to_string())

# ── 3D. Custom lambda inside agg ────────────────────────────
print("\n[3D] agg with custom lambda — Revenue range (max-min) per Category:")
result_3d = df.groupby('Category')['Revenue'].agg(
    lambda x: x.max() - x.min()
).round(2)
result_3d.name = 'Revenue_Range'
print(result_3d)

print()

# ============================================================
print("=" * 65)
print("  SECTION 4: apply() ON GROUPS")
print("=" * 65)
# apply() passes each GROUP (as DataFrame) to your function
# More flexible than agg() — can return any shape

# ── 4A. Custom function returning a scalar ───────────────────
def revenue_coefficient_of_variation(group):
    """CV = std/mean * 100 — measures revenue consistency"""
    return round((group['Revenue'].std() / group['Revenue'].mean()) * 100, 2)

print("\n[4A] Revenue Coefficient of Variation per Category:")
cv_result = df.groupby('Category').apply(revenue_coefficient_of_variation)
cv_result.name = 'Revenue_CV_%'
print(cv_result.sort_values())
print("  → Lower CV = more consistent sales revenue")

# ── 4B. Group-wise ranking — using transform ─────────────────
# transform() is the right tool for group-wise element operations
# It returns a Series with the SAME INDEX as the original df
# Perfect for ranking, normalizing, z-scoring within groups
print("\n[4B] Rank each sale by Revenue within its Category (using transform):")
df['Rank_in_Category'] = (df.groupby('Category')['Revenue']
                            .transform(lambda x: x.rank(ascending=False, method='dense')))
print(df[['Category', 'Product', 'Revenue', 'Rank_in_Category']]
      .sort_values(['Category', 'Rank_in_Category'])
      .head(10).to_string())
# Why transform? apply() drops the groupby key column in newer pandas.
# transform() keeps the original df structure — result aligns with original rows.

# ── 4C. Group-wise normalization — using transform ───────────
print("\n[4C] Min-Max Normalization of Revenue within each Category (transform):")
df['Revenue_Normalized'] = (df.groupby('Category')['Revenue']
                              .transform(lambda x: ((x - x.min()) / (x.max() - x.min())).round(4)))
print(df[['Category', 'Product', 'Revenue', 'Revenue_Normalized']]
      .sort_values('Category')
      .head(10).to_string())
print("  → 1.0 = highest earner in its category; 0.0 = lowest")

# ── 4D. apply returning a Series (custom summary) ───────────
def category_summary(group):
    return pd.Series({
        'Total_Revenue':   round(group['Revenue'].sum(), 2),
        'Avg_Revenue':     round(group['Revenue'].mean(), 2),
        'Best_Product':    group.loc[group['Revenue'].idxmax(), 'Product'],
        'Top_Salesperson': group.groupby('Salesperson')['Revenue'].sum().idxmax(),
        'Num_Transactions':len(group),
    })

print("\n[4D] apply() returning a Series — rich category summary:")
summary = df.groupby('Category').apply(category_summary)
print(summary.to_string())

# ── 4E. Looping over groups ──────────────────────────────────
print("\n[4E] Looping over groups with for name, group in grp:")
for name, group in df.groupby('Region'):
    top_sale = group.loc[group['Revenue'].idxmax()]
    print(f"  {name:6s} | Rows: {len(group):3d} | "
          f"Total Revenue: ₹{group['Revenue'].sum():>10,.2f} | "
          f"Best Sale: {top_sale['Product']} (₹{top_sale['Revenue']:,.2f})")

print()

# ============================================================
print("=" * 65)
print("  SECTION 5: REAL BUSINESS ANALYSIS — Top Performers")
print("=" * 65)

# ── Top product per category ─────────────────────────────────
print("\n[5A] Top Product (by total Revenue) in each Category:")
top_products = (df.groupby(['Category', 'Product'])['Revenue']
                  .sum()
                  .reset_index()
                  .sort_values('Revenue', ascending=False)
                  .groupby('Category')
                  .first()
                  .rename(columns={'Revenue': 'Total_Revenue', 'Product': 'Top_Product'}))
# Note: after sort+groupby first, we get the top per category
top_by_cat = (df.groupby(['Category', 'Product'])['Revenue']
               .sum()
               .reset_index()
               .sort_values('Revenue', ascending=False))
result = top_by_cat.groupby('Category').first().reset_index()
result.columns = ['Category', 'Top_Product', 'Revenue']
print(result.to_string(index=False))

# ── Salesperson leaderboard ──────────────────────────────────
print("\n[5B] Salesperson Leaderboard — Total Revenue:")
leaderboard = df.groupby('Salesperson').agg(
    Total_Revenue    = ('Revenue', 'sum'),
    Total_Units      = ('Units', 'sum'),
    Transactions     = ('Revenue', 'count'),
    Avg_Deal_Size    = ('Revenue', 'mean'),
    Categories_Sold  = ('Category', 'nunique'),
).round(2).sort_values('Total_Revenue', ascending=False)
print(leaderboard.to_string())

# ── Monthly revenue trend ────────────────────────────────────
print("\n[5C] Monthly Revenue Totals (sorted by month):")
month_order = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
monthly = df.groupby('Month')['Revenue'].sum().round(2)
monthly = monthly.reindex(month_order)
for m, rev in monthly.items():
    bar = '█' * int(rev // 500)
    print(f"  {m:3s}: ₹{rev:>9,.2f}  {bar}")

print()
print("✅ groupby_demo.py complete!")
