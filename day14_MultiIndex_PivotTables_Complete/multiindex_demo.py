# ============================================================
# DAY 14 — MultiIndex + Wide/Long Format + melt()
# ============================================================
# Topics:
#   - What is MultiIndex & why it exists
#   - from_tuples, from_product, from_arrays
#   - MultiIndex on ROWS (index) and COLUMNS
#   - Selecting from MultiIndex (.loc with tuples, xs())
#   - stack() and unstack()
#   - swaplevel() and sort_index()
#   - transpose (.T)
#   - Wide vs Long format — when to use which
#   - melt() — id_vars, var_name, value_name
# ============================================================

import pandas as pd
import numpy as np

pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 120)

print("=" * 70)
print("  SECTION 1: WHAT IS MULTIINDEX?")
print("=" * 70)

# ── Why MultiIndex? ──────────────────────────────────────────
# Normal Index: one label per row/col  →  works for 1D hierarchies
# MultiIndex:  multiple labels per row →  works for 2D+ hierarchies
#
# Think of it like a folder structure:
#   City > Year > Month (3 levels of indexing)
#   Instead of one index col, you have a TUPLE as the key
#
# Real-world use:
#   - Financial data: (Stock, Date)
#   - Census data:    (Country, State, City)
#   - Experiments:    (Subject, Trial, Measurement)
#   - Sales:          (Region, Category, Product)

print("""
MultiIndex = hierarchical / nested labelling for rows or columns.

  Normal Index:           MultiIndex:
  ──────────────          ──────────────────────
  'Delhi'  → row 0        ('Delhi', 2022) → row 0
  'Mumbai' → row 1        ('Delhi', 2023) → row 1
  'Pune'   → row 2        ('Mumbai', 2022) → row 2
                           ('Mumbai', 2023) → row 3

  One label per row       Tuple of labels per row
  Flat structure          Hierarchical / nested structure
""")


# ============================================================
print("=" * 70)
print("  SECTION 2: CREATING MULTIINDEX")
print("=" * 70)

# ── 2A. from_tuples ──────────────────────────────────────────
# Manual: give a list of tuples, each tuple = one row label
print("\n[2A] MultiIndex.from_tuples:")
tuples = [
    ('Delhi',   2022), ('Delhi',   2023),
    ('Mumbai',  2022), ('Mumbai',  2023),
    ('Chennai', 2022), ('Chennai', 2023),
]
mi_tuples = pd.MultiIndex.from_tuples(tuples, names=['City', 'Year'])
print(mi_tuples)
print(f"  Length: {len(mi_tuples)}  |  nlevels: {mi_tuples.nlevels}")
print(f"  levels: {mi_tuples.levels}")
print(f"  names:  {mi_tuples.names}")

# ── 2B. from_product ─────────────────────────────────────────
# Cartesian product — all combinations of given lists
# Most convenient when you want ALL combos
print("\n[2B] MultiIndex.from_product (Cartesian product):")
cities  = ['Delhi', 'Mumbai', 'Chennai']
years   = [2022, 2023]
mi_prod = pd.MultiIndex.from_product([cities, years], names=['City', 'Year'])
print(mi_prod)
print(f"  {len(cities)} cities × {len(years)} years = {len(mi_prod)} index entries")

# ── 2C. from_arrays ──────────────────────────────────────────
# Provide each level as a separate array (parallel arrays)
print("\n[2C] MultiIndex.from_arrays:")
cities_arr = ['Delhi', 'Delhi', 'Mumbai', 'Mumbai']
years_arr  = [2022,    2023,    2022,     2023   ]
mi_arrays  = pd.MultiIndex.from_arrays([cities_arr, years_arr], names=['City', 'Year'])
print(mi_arrays)


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 3: MULTIINDEX SERIES")
print("=" * 70)

# Create a MultiIndex Series — population data
pop_data = [32.1, 33.8, 20.7, 21.6, 11.2, 11.9]
pop = pd.Series(pop_data, index=mi_tuples, name='Population_Millions')
pop = pop.sort_index()   # MultiIndex must be sorted for reliable slicing

print("\n[3A] MultiIndex Series — City/Year Population:")
print(pop)

# ── Accessing elements ────────────────────────────────────────
print("\n[3B] Accessing — pop['Delhi']:  (all Delhi entries)")
print(pop['Delhi'])

print("\n[3C] Accessing — pop['Delhi', 2023]: (specific)")
print(pop['Delhi', 2023])

print("\n[3D] Accessing — pop.loc[('Mumbai', 2022):]  (requires sorted index)")
print(pop.loc[('Mumbai', 2022):])

# ── xs() — cross-section ─────────────────────────────────────
# xs = cross-section: select by a specific label at a specific level
print("\n[3E] xs() — cross-section for year 2022 (level='Year'):")
print(pop.xs(2022, level='Year'))

print("\n[3F] xs() — cross-section for 'Mumbai' (level='City'):")
print(pop.xs('Mumbai', level='City'))


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 4: MULTIINDEX DATAFRAME — ROWS")
print("=" * 70)

# City + Year as MultiIndex rows
np.random.seed(42)

cities_full = ['Delhi', 'Mumbai', 'Chennai', 'Kolkata']
years_full  = [2021, 2022, 2023]
mi_full     = pd.MultiIndex.from_product([cities_full, years_full], names=['City', 'Year'])

df_city = pd.DataFrame({
    'Population_M': np.round(np.random.uniform(5, 35, len(mi_full)), 1),
    'GDP_Billion':  np.round(np.random.uniform(50, 500, len(mi_full)), 1),
    'Unemployment': np.round(np.random.uniform(3, 12, len(mi_full)), 2),
    'Inflation':    np.round(np.random.uniform(2, 8, len(mi_full)), 2),
}, index=mi_full)

print("\n[4A] DataFrame with MultiIndex rows (City × Year):")
print(df_city)

# ── Selection ─────────────────────────────────────────────────
print("\n[4B] df_city.loc['Delhi'] — all Delhi rows:")
print(df_city.loc['Delhi'])

print("\n[4C] df_city.loc[('Delhi', 2022)] — specific row:")
print(df_city.loc[('Delhi', 2022)])

print("\n[4D] df_city.loc[('Delhi', 2022), 'GDP_Billion'] — single cell:")
print(df_city.loc[('Delhi', 2022), 'GDP_Billion'])

print("\n[4E] xs() — all cities for Year=2022:")
print(df_city.xs(2022, level='Year'))

print("\n[4F] xs() — all years for Chennai:")
print(df_city.xs('Chennai', level='City'))

# ── Selecting a range of outer level ─────────────────────────
print("\n[4G] loc with list of outer labels:")
print(df_city.loc[['Delhi', 'Mumbai']])


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 5: MULTIINDEX ON COLUMNS")
print("=" * 70)

# MultiIndex columns — useful for multi-category data side by side
# e.g. Sales and Returns for each product category
categories = ['Electronics', 'Clothing', 'Groceries']
metrics    = ['Revenue', 'Units', 'Returns']

col_mi = pd.MultiIndex.from_product([categories, metrics], names=['Category', 'Metric'])

np.random.seed(7)
df_cols = pd.DataFrame(
    np.round(np.random.uniform(100, 5000, (4, len(col_mi))), 1),
    index  = pd.Index(['Q1', 'Q2', 'Q3', 'Q4'], name='Quarter'),
    columns= col_mi
)

print("\n[5A] DataFrame with MultiIndex COLUMNS:")
print(df_cols)

# ── Selecting MultiIndex columns ──────────────────────────────
print("\n[5B] Select entire 'Electronics' category:")
print(df_cols['Electronics'])

print("\n[5C] Select 'Revenue' from 'Clothing':")
print(df_cols['Clothing']['Revenue'])
# equivalently: df_cols[('Clothing', 'Revenue')]

print("\n[5D] Select 'Revenue' across ALL categories (cross-section on axis=1):")
print(df_cols.xs('Revenue', level='Metric', axis=1))


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 6: STACK AND UNSTACK")
print("=" * 70)

# ── stack() — columns → rows (wide → long) ───────────────────
# Moves innermost column level DOWN to innermost index level
print("""
stack() and unstack() are inverses of each other:

  UNSTACK:  move a row-index level → column level  (long → wide)
  STACK:    move a column level   → row-index level (wide → long)

Think: stack() = "stack" the columns on top of each other as rows
""")

# Simple example first
df_simple = pd.DataFrame({
    'Math': [90, 85, 78],
    'Science': [88, 92, 81],
    'English': [76, 88, 95],
}, index=pd.Index(['Alice', 'Bob', 'Carol'], name='Student'))

print("[6A] Wide DataFrame (students × subjects):")
print(df_simple)

print("\n[6B] After stack() — moves Subject column into index:")
stacked = df_simple.stack()
stacked.name = 'Score'
print(stacked)
print(f"\n  Wide shape: {df_simple.shape}  →  Long shape: {stacked.shape}")
print("  Index is now MultiIndex: (Student, Subject)")

print("\n[6C] After unstack() — back to wide format:")
unstacked = stacked.unstack()
print(unstacked)
print("  ✅ Identical to original df_simple")

# ── unstack on MultiIndex row DataFrame ──────────────────────
print("\n[6D] Unstack on df_city — Year level → columns:")
df_unstacked = df_city['GDP_Billion'].unstack(level='Year')
print(df_unstacked)
print("  ✅ Each city is a row, each year is a column — like a pivot!")

print("\n[6E] Unstack level 'City' — Cities become columns:")
df_unstacked_city = df_city['Population_M'].unstack(level='City')
print(df_unstacked_city)

print("\n[6F] stack() on MultiIndex column DataFrame (df_cols):")
df_stacked_cols = df_cols.stack(level='Category')
print(df_stacked_cols)
print(f"  Shape: {df_cols.shape} → {df_stacked_cols.shape}")


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 7: SWAPLEVEL AND SORT_INDEX")
print("=" * 70)

print("\n[7A] df_city original index levels: City (outer) → Year (inner)")
print(df_city.head(6))

# swaplevel — swap which level is outer and which is inner
df_swapped = df_city.swaplevel('City', 'Year')
print("\n[7B] After swaplevel — Year (outer) → City (inner):")
print(df_swapped.head(6))
print("  ⚠️  Notice index is NOT sorted after swaplevel!")

# sort_index — mandatory after swaplevel for clean lookups
df_swapped_sorted = df_swapped.sort_index()
print("\n[7C] After sort_index() — clean sorted order:")
print(df_swapped_sorted)

# Now you can query by year as the outer level
print("\n[7D] Access year 2022 after swaplevel + sort_index:")
print(df_swapped_sorted.loc[2022])

# sort_index on specific level
print("\n[7E] sort_index(level='City') — sort by City regardless:")
print(df_city.sort_index(level='City'))


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 8: TRANSPOSE (.T)")
print("=" * 70)

print("\n[8A] Original df_cols (4 rows × 9 cols):")
print(f"  Shape: {df_cols.shape}")

print("\n[8B] After .T — rows and columns are SWAPPED:")
df_T = df_cols.T
print(df_T)
print(f"  Shape: {df_T.shape}")
print("""
  When to use .T:
  - View or compute across what were previously columns
  - Convert row-oriented data to column-oriented
  - Convenient when your data's "natural" shape is the transpose
""")


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 9: WIDE vs LONG FORMAT")
print("=" * 70)

print("""
TWO WAYS to store the same data:

  WIDE FORMAT (human-readable):          LONG FORMAT (machine-friendly):
  ─────────────────────────────          ────────────────────────────────
  Name   Math  Science  English          Name   Subject  Score
  Alice   90     88       76             Alice  Math       90
  Bob     85     92       88             Alice  Science    88
  Carol   78     81       95             Alice  English    76
                                         Bob    Math       85
                                         ...

  ✅ Easy to read for humans              ✅ Required by most ML libraries
  ✅ Compact (fewer rows)                 ✅ Easy to filter/group
  ❌ Hard to group/aggregate by subject   ✅ Seaborn/Plotly expect this
  ❌ Many NaNs when data is sparse        ✅ Tidy data format
""")

# Concrete wide DataFrame
df_wide = pd.DataFrame({
    'Student': ['Alice', 'Bob', 'Carol', 'Dave'],
    'City':    ['Delhi', 'Mumbai', 'Delhi', 'Chennai'],
    'Math':    [90, 85, 78, 92],
    'Science': [88, 92, 81, 79],
    'English': [76, 88, 95, 83],
})
print("[9A] Wide Format:")
print(df_wide)


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 10: melt() — WIDE TO LONG")
print("=" * 70)
# melt() converts wide → long
# id_vars:    columns to KEEP as-is (identifier columns)
# value_vars: columns to MELT (if None → all non-id columns)
# var_name:   name for the new "variable" column
# value_name: name for the new "value" column

print("""
pd.melt(df,
    id_vars=['Student', 'City'],   # keep these as row identifiers
    value_vars=['Math','Science','English'],  # these columns get "melted"
    var_name='Subject',            # new col: was the column name
    value_name='Score'             # new col: was the cell value
)
""")

df_long = pd.melt(
    df_wide,
    id_vars   = ['Student', 'City'],
    value_vars = ['Math', 'Science', 'English'],
    var_name  = 'Subject',
    value_name= 'Score',
)
print("[10A] Long Format after melt():")
print(df_long.sort_values(['Student', 'Subject']).reset_index(drop=True))

print(f"\n  Wide shape: {df_wide.shape}  →  Long shape: {df_long.shape}")
print("  Rows went from 4 to 12 (4 students × 3 subjects)")

# ── Practical use: analysis is now easy ──────────────────────
print("\n[10B] With long format — easy subject-wise stats:")
print(df_long.groupby('Subject')['Score'].agg(['mean', 'max', 'min']).round(1))

print("\n[10C] With long format — easy city-wise analysis:")
print(df_long.groupby('City')['Score'].mean().round(1))

# ── melt with only some columns ──────────────────────────────
print("\n[10D] Partial melt — only Math and Science:")
df_partial = pd.melt(
    df_wide,
    id_vars   = ['Student'],
    value_vars = ['Math', 'Science'],    # English NOT included
    var_name  = 'Subject',
    value_name= 'Score',
)
print(df_partial)

# ── Going back: pivot() — long to wide ───────────────────────
print("\n[10E] Reverse: pivot() — long back to wide:")
df_back = df_long.pivot(index='Student', columns='Subject', values='Score')
df_back.columns.name = None   # remove 'Subject' label from column axis
df_back = df_back.reset_index()
print(df_back)
print("  ✅ Back to wide format!")


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 11: COMPLETE MULTIINDEX WORKFLOW EXAMPLE")
print("=" * 70)

# Build a quarterly sales MultiIndex DataFrame
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
regions  = ['North', 'South', 'East', 'West']
mi_qr    = pd.MultiIndex.from_product([regions, quarters], names=['Region', 'Quarter'])

np.random.seed(99)
df_qr = pd.DataFrame({
    'Electronics': np.random.randint(500, 5000, len(mi_qr)),
    'Clothing':    np.random.randint(200, 2000, len(mi_qr)),
    'Groceries':   np.random.randint(100, 1500, len(mi_qr)),
}, index=mi_qr)

print("\n[11A] Region × Quarter MultiIndex DataFrame:")
print(df_qr)

print("\n[11B] Total sales per Region (sum across quarters):")
print(df_qr.groupby(level='Region').sum())

print("\n[11C] Average per Quarter (mean across regions):")
print(df_qr.groupby(level='Quarter').mean().round(0))

print("\n[11D] Unstack Quarter → make wide Region × Quarter:")
wide_qr = df_qr['Electronics'].unstack('Quarter')
print(wide_qr)

print("\n[11E] Stack back → long format:")
long_qr = wide_qr.stack()
long_qr.name = 'Electronics_Revenue'
print(long_qr.head(8))

print("\n[11F] Find best quarter for each region:")
for region in regions:
    region_data = df_qr.loc[region, 'Electronics']
    best_q = region_data.idxmax()
    print(f"  {region:6s}: best quarter = {best_q} ({region_data[best_q]:,})")

print()
print("✅ multiindex_demo.py complete!")
