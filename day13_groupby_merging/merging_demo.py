# ============================================================
# DAY 13 — PANDAS Concatenation, Merging & Joining
# ============================================================
# Dataset: Synthetic Customers + Orders + Products tables
# Topics covered:
#   - pd.concat (vertical, horizontal, ignore_index, keys)
#   - df.append (deprecated but explained)
#   - pd.merge (inner, left, right, outer)
#   - self join
#   - left_on / right_on (different column names)
#   - merge with suffixes
#   - np.intersect1d and np.setdiff1d
# ============================================================

import pandas as pd
import numpy as np

print("=" * 65)
print("  BUILDING SAMPLE DATASETS")
print("=" * 65)

# ── Customers Table ──────────────────────────────────────────
customers = pd.DataFrame({
    'customer_id':   [1, 2, 3, 4, 5, 6],
    'name':          ['Aisha', 'Rohan', 'Priya', 'Karan', 'Deepa', 'Arjun'],
    'city':          ['Delhi', 'Mumbai', 'Bangalore', 'Delhi', 'Chennai', 'Hyderabad'],
    'member_tier':   ['Gold', 'Silver', 'Gold', 'Bronze', 'Silver', 'Bronze'],
    'join_year':     [2020, 2021, 2019, 2022, 2020, 2023],
})

# ── Orders Table ─────────────────────────────────────────────
# Note: customers 5 & 6 have NO orders (for left/outer join demo)
# Orders has customer_id 7 which doesn't exist in customers (for right/outer join demo)
orders = pd.DataFrame({
    'order_id':    [101, 102, 103, 104, 105, 106, 107, 108],
    'customer_id': [  1,   2,   1,   3,   2,   4,   7,   7],  # 7 = unknown customer
    'product':     ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Charger',
                    'Speaker', 'Keyboard', 'Mouse'],
    'amount':      [55000, 22000, 35000, 8000, 1500, 4500, 3200, 900],
    'status':      ['Delivered', 'Delivered', 'Shipped', 'Delivered',
                    'Cancelled', 'Delivered', 'Delivered', 'Shipped'],
})

# ── Products Table ───────────────────────────────────────────
products = pd.DataFrame({
    'product_name': ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Speaker', 'Monitor'],
    'category':     ['Electronics', 'Electronics', 'Electronics',
                     'Accessories', 'Accessories', 'Electronics'],
    'price':        [55000, 22000, 35000, 8000, 4500, 18000],
    'stock':        [50, 200, 80, 150, 120, 30],
})

# ── New Customers batch (for concat demo) ────────────────────
new_customers = pd.DataFrame({
    'customer_id': [7, 8, 9],
    'name':        ['Vikram', 'Sneha', 'Raj'],
    'city':        ['Pune', 'Kolkata', 'Jaipur'],
    'member_tier': ['Gold', 'Silver', 'Gold'],
    'join_year':   [2023, 2023, 2024],
})

print("\nCustomers Table:")
print(customers.to_string(index=False))
print("\nOrders Table:")
print(orders.to_string(index=False))
print("\nProducts Table:")
print(products.to_string(index=False))

print()

# ============================================================
print("=" * 65)
print("  SECTION 1: pd.concat — CONCATENATION")
print("=" * 65)

# ── 1A. Vertical concat (stack rows) ────────────────────────
# axis=0 (default) → stack on top of each other
# All DataFrames must have the same columns
print("\n[1A] Vertical concat — add new_customers to customers:")
all_customers = pd.concat([customers, new_customers], axis=0)
print(all_customers.to_string())
print(f"\n   Original: {len(customers)} rows | New: {len(new_customers)} rows | Combined: {len(all_customers)} rows")
print("   ⚠️  Notice index still has 0,1,2... repeated from new_customers!")

# ── 1B. ignore_index=True — reset the index ─────────────────
print("\n[1B] With ignore_index=True — clean index after concat:")
all_customers_clean = pd.concat([customers, new_customers], axis=0, ignore_index=True)
print(all_customers_clean.to_string())
print("   ✅ Index now continuous: 0,1,2...8")

# ── 1C. keys — label the source of each chunk ───────────────
print("\n[1C] keys=['old', 'new'] — MultiIndex showing source:")
labeled = pd.concat([customers, new_customers], keys=['Existing', 'New'])
print(labeled.to_string())
print("\n   Access 'Existing' group: labeled.loc['Existing']")
print(labeled.loc['Existing'].to_string())

# ── 1D. Horizontal concat (join columns side by side) ────────
# axis=1 → put columns next to each other (row indices must align)
print("\n[1D] Horizontal concat — axis=1 (side by side):")
extra_info = pd.DataFrame({
    'loyalty_points': [1200, 450, 2300, 150, 800, 90],
    'preferred_pay':  ['UPI', 'Card', 'UPI', 'Cash', 'Card', 'UPI'],
})
customers_extended = pd.concat([customers, extra_info], axis=1)
print(customers_extended.to_string(index=False))

# ── 1E. Concat with mismatched columns ──────────────────────
print("\n[1E] Concat with mismatched columns — NaN fills the gaps:")
df_a = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df_b = pd.DataFrame({'B': [5, 6], 'C': [7, 8]})
mismatched = pd.concat([df_a, df_b], ignore_index=True)
print(mismatched)
print("   Column A: only in df_a → NaN for df_b rows")
print("   Column C: only in df_b → NaN for df_a rows")

# ── 1F. join='inner' — keep only common columns ─────────────
print("\n[1F] join='inner' — only keep columns common to both:")
inner_concat = pd.concat([df_a, df_b], join='inner', ignore_index=True)
print(inner_concat)
print("   Only column B survived (common to both)")

print()

# ============================================================
print("=" * 65)
print("  SECTION 2: pd.merge — ALL JOIN TYPES")
print("=" * 65)
# SQL equivalent:
#   INNER JOIN → how='inner'  → only matching rows
#   LEFT JOIN  → how='left'   → all left + matching right
#   RIGHT JOIN → how='right'  → all right + matching left
#   OUTER JOIN → how='outer'  → all rows from both

# ── 2A. INNER JOIN ──────────────────────────────────────────
# Keep ONLY rows where customer_id exists in BOTH tables
print("\n[2A] INNER JOIN — customers ⋈ orders (only matched rows):")
inner = pd.merge(customers, orders, on='customer_id', how='inner')
print(inner[['name', 'city', 'order_id', 'product', 'amount']].to_string(index=False))
print(f"\n   customers: {len(customers)} rows | orders: {len(orders)} rows | inner: {len(inner)} rows")
print("   ✅ Only customers WHO HAVE ORDERS appear")
print("   ✅ Order with customer_id=7 (unknown) is EXCLUDED")
print("   ✅ Customers 5 & 6 (no orders) are EXCLUDED")

# ── 2B. LEFT JOIN ───────────────────────────────────────────
# Keep ALL rows from LEFT table (customers)
# If no match in right → NaN
print("\n[2B] LEFT JOIN — all customers, even without orders:")
left = pd.merge(customers, orders, on='customer_id', how='left')
print(left[['name', 'city', 'order_id', 'product', 'amount']].to_string(index=False))
print(f"\n   customers: {len(customers)} | orders: {len(orders)} | left: {len(left)} rows")
print("   ✅ Deepa & Arjun (no orders) appear with NaN in order columns")
print("   ✅ customer_id=7 order NOT included (not in left/customers)")

# ── 2C. RIGHT JOIN ──────────────────────────────────────────
# Keep ALL rows from RIGHT table (orders)
# If no match in left → NaN
print("\n[2C] RIGHT JOIN — all orders, even from unknown customers:")
right = pd.merge(customers, orders, on='customer_id', how='right')
print(right[['name', 'city', 'order_id', 'product', 'amount']].to_string(index=False))
print(f"\n   customers: {len(customers)} | orders: {len(orders)} | right: {len(right)} rows")
print("   ✅ Orders 107 & 108 (customer_id=7, unknown) appear with NaN in customer cols")

# ── 2D. OUTER JOIN (FULL OUTER) ─────────────────────────────
# Keep ALL rows from BOTH tables
# No match on either side → NaN
print("\n[2D] OUTER JOIN — all customers AND all orders:")
outer = pd.merge(customers, orders, on='customer_id', how='outer')
print(outer[['customer_id', 'name', 'city', 'order_id', 'product', 'amount']].to_string(index=False))
print(f"\n   customers: {len(customers)} | orders: {len(orders)} | outer: {len(outer)} rows")
print("   ✅ All customers appear (incl. Deepa, Arjun with no orders)")
print("   ✅ All orders appear (incl. orders from customer_id=7)")

print()

# ============================================================
print("=" * 65)
print("  SECTION 3: MERGE VARIANTS")
print("=" * 65)

# ── 3A. left_on / right_on — different column names ─────────
# When the join columns have DIFFERENT NAMES in each DataFrame
print("\n[3A] left_on / right_on — different column names:")
orders_renamed = orders.rename(columns={'customer_id': 'cust_id'})
merged_diff = pd.merge(
    customers, orders_renamed,
    left_on='customer_id',     # column name in LEFT df
    right_on='cust_id',        # column name in RIGHT df
    how='inner'
)
print(merged_diff[['customer_id', 'cust_id', 'name', 'product', 'amount']].to_string(index=False))
print("   Both customer_id and cust_id appear — you can drop one:")
merged_diff = merged_diff.drop(columns=['cust_id'])
print("   After drop: columns =", merged_diff.columns.tolist())

# ── 3B. suffixes — handle duplicate column names ─────────────
print("\n[3B] suffixes — when both DataFrames share a non-key column name:")
# orders has 'product' as text; let's create overlap scenario
customers_with_note = customers.copy()
customers_with_note['status'] = ['Active', 'Active', 'VIP', 'Inactive', 'Active', 'New']
# Now both customers_with_note and orders have 'status'
merged_suffix = pd.merge(
    customers_with_note, orders,
    on='customer_id',
    how='inner',
    suffixes=('_customer', '_order')   # resolve name clash
)
print(merged_suffix[['name', 'status_customer', 'status_order', 'amount']].to_string(index=False))

# ── 3C. Chained merge — 3 tables ────────────────────────────
print("\n[3C] Chained merge — customers → orders → products:")
merged_3 = (pd.merge(customers, orders, on='customer_id', how='inner')
              .merge(products, left_on='product', right_on='product_name', how='left'))
print(merged_3[['name', 'product', 'amount', 'category', 'stock']].to_string(index=False))

# ── 3D. Self join — employee/manager hierarchy example ───────
print("\n[3D] Self Join — employee-manager hierarchy:")
employees = pd.DataFrame({
    'emp_id':    [1, 2, 3, 4, 5],
    'emp_name':  ['Aisha', 'Rohan', 'Priya', 'Karan', 'Deepa'],
    'manager_id':[np.nan, 1, 1, 2, 2],      # Aisha has no manager (CEO)
})
self_joined = pd.merge(
    employees,
    employees[['emp_id', 'emp_name']],    # right = same table
    left_on='manager_id',
    right_on='emp_id',
    how='left',
    suffixes=('', '_manager')
).rename(columns={'emp_name_manager': 'manager_name'})
print(self_joined[['emp_id', 'emp_name', 'manager_id', 'manager_name']].to_string(index=False))
print("   ✅ Aisha (CEO) shows NaN manager — correct!")

# ── 3E. Alternative: DataFrame.merge() syntax ───────────────
print("\n[3E] Alternate syntax — df.merge() instead of pd.merge():")
result_3e = customers.merge(orders, on='customer_id', how='inner')
print(f"   customers.merge(orders) — same result as pd.merge()!")
print(f"   Shape: {result_3e.shape}")

print()

# ============================================================
print("=" * 65)
print("  SECTION 4: np.intersect1d and np.setdiff1d")
print("=" * 65)
# These operate on ARRAYS/SERIES — useful for finding common/different IDs

cust_ids  = customers['customer_id'].values    # [1,2,3,4,5,6]
order_ids = orders['customer_id'].unique()      # [1,2,3,4,7]

print(f"\nCustomer IDs in Customers table: {cust_ids}")
print(f"Customer IDs in Orders table:    {order_ids}")

# ── 4A. intersect1d — common elements ───────────────────────
common = np.intersect1d(cust_ids, order_ids)
print(f"\n[4A] np.intersect1d — IDs present in BOTH tables:")
print(f"   {common}")
print(f"   → These customers have placed orders (= INNER JOIN keys)")

# ── 4B. setdiff1d — elements in A but not in B ───────────────
only_customers = np.setdiff1d(cust_ids, order_ids)
print(f"\n[4B] np.setdiff1d(customers, orders) — in customers but NOT in orders:")
print(f"   {only_customers}")
print(f"   → These customers have NEVER placed an order")

only_orders = np.setdiff1d(order_ids, cust_ids)
print(f"\n[4C] np.setdiff1d(orders, customers) — in orders but NOT in customers:")
print(f"   {only_orders}")
print(f"   → These are GHOST orders (customer doesn't exist in our DB!)")

# ── 4D. union1d — all unique elements ────────────────────────
all_ids = np.union1d(cust_ids, order_ids)
print(f"\n[4D] np.union1d — all unique IDs from both tables:")
print(f"   {all_ids}")
print(f"   → OUTER JOIN would produce rows for all of these")

# ── 4E. Practical use: filter based on intersection ─────────
print("\n[4E] Practical: get customer info for IDs in both tables:")
valid_ids = np.intersect1d(cust_ids, order_ids)
filtered = customers[customers['customer_id'].isin(valid_ids)]
print(filtered[['customer_id', 'name', 'member_tier']].to_string(index=False))

print()

# ============================================================
print("=" * 65)
print("  SECTION 5: FULL BUSINESS CASE — Join + Group Analysis")
print("=" * 65)
# Business Question: Which city generates most revenue from Delivered orders?

print("\n[5A] Delivered orders revenue by City:")
delivered = pd.merge(customers, orders, on='customer_id', how='inner')
delivered = delivered[delivered['status'] == 'Delivered']
city_revenue = (delivered.groupby('city')['amount']
                          .agg(['sum', 'count', 'mean'])
                          .round(2)
                          .rename(columns={'sum': 'Total_Revenue',
                                           'count': 'Num_Orders',
                                           'mean': 'Avg_Order'})
                          .sort_values('Total_Revenue', ascending=False))
print(city_revenue.to_string())

print("\n[5B] Revenue by Member Tier (only Delivered orders):")
tier_analysis = (delivered.groupby('member_tier')
                           .agg(
                               Total_Revenue = ('amount', 'sum'),
                               Avg_Order     = ('amount', 'mean'),
                               Num_Orders    = ('amount', 'count'),
                           )
                           .round(2)
                           .sort_values('Total_Revenue', ascending=False))
print(tier_analysis.to_string())

print("\n[5C] Top customer by total spending:")
top_spenders = (pd.merge(customers, orders, on='customer_id', how='inner')
                  .groupby(['customer_id', 'name', 'member_tier'])['amount']
                  .sum()
                  .reset_index()
                  .sort_values('amount', ascending=False))
top_spenders.columns = ['ID', 'Name', 'Tier', 'Total_Spend']
print(top_spenders.to_string(index=False))

print()
print("=" * 65)
print("  JOIN TYPES CHEATSHEET (SQL ↔ Pandas)")
print("=" * 65)
cheatsheet = pd.DataFrame({
    'SQL':    ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL OUTER JOIN'],
    'Pandas': ["how='inner'", "how='left'", "how='right'", "how='outer'"],
    'Result': [
        'Only matching rows',
        'All left + matching right (NaN for no match)',
        'All right + matching left (NaN for no match)',
        'All rows from both (NaN where no match)',
    ]
})
print(cheatsheet.to_string(index=False))

print()
print("✅ merging_demo.py complete!")
