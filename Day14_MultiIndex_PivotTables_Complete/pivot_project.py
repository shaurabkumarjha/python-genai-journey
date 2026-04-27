# ============================================================
# DAY 14 — PIVOT TABLES: E-Commerce Sales Analysis
# ============================================================
# Complete Mini-Project:
#   1. Generate realistic e-commerce sales dataset
#   2. pivot_table: all parameters explained
#   3. Multi-dimensional pivots
#   4. margins=True (row/col totals)
#   5. Multiple aggfuncs
#   6. Visualizations: heatmap, bar chart, trend lines
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')           # non-interactive backend (works without display)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.float_format', '{:,.1f}'.format)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 130)

# ============================================================
print("=" * 70)
print("  SECTION 1: PIVOT TABLE THEORY")
print("=" * 70)
print("""
pivot_table() is a super-powered groupby + unstack in one call.

pd.pivot_table(df,
    values   = 'Revenue',          # what to aggregate
    index    = 'Month',            # row grouping
    columns  = 'Category',         # column grouping
    aggfunc  = 'sum',              # how to aggregate (sum/mean/count/...)
    fill_value = 0,                # replace NaN with this
    margins  = True,               # add All row/col (grand totals)
    margins_name = 'Grand Total',  # label for margins row/col
)

Think of it as:
  → index   = SQL GROUP BY (rows)
  → columns = PIVOT the category values into columns
  → values  = what number goes in each cell
  → aggfunc = how to handle multiple records per cell
""")

# ============================================================
print("=" * 70)
print("  SECTION 2: GENERATE E-COMMERCE SALES DATASET")
print("=" * 70)

np.random.seed(42)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_num = {m: i+1 for i, m in enumerate(months)}

categories = ['Electronics', 'Fashion', 'Home & Kitchen', 'Books', 'Sports', 'Beauty']
regions    = ['North', 'South', 'East', 'West']
channels   = ['App', 'Website', 'Store']
genders    = ['Male', 'Female', 'Other']

# Revenue weights — seasonal + category patterns
base_rev = {
    'Electronics':     3000, 'Fashion':       1500,
    'Home & Kitchen':  1200, 'Books':          400,
    'Sports':          800,  'Beauty':         600,
}
season_mult = {
    'Jan': 0.8, 'Feb': 0.7, 'Mar': 0.9, 'Apr': 1.0,
    'May': 1.1, 'Jun': 1.0, 'Jul': 0.9, 'Aug': 1.0,
    'Sep': 1.1, 'Oct': 1.2, 'Nov': 1.8, 'Dec': 2.0,  # Diwali + Christmas spike
}

n = 2500
month_col    = np.random.choice(months, n, p=[1/12]*12)
cat_col      = np.random.choice(categories, n)
region_col   = np.random.choice(regions, n)
channel_col  = np.random.choice(channels, n, p=[0.5, 0.35, 0.15])
gender_col   = np.random.choice(genders, n, p=[0.45, 0.50, 0.05])
units_col    = np.random.randint(1, 15, n)

revenue_col = np.array([
    round(base_rev[cat] * season_mult[month] * units * np.random.uniform(0.7, 1.4), 2)
    for cat, month, units in zip(cat_col, month_col, units_col)
])
discount_col = np.round(revenue_col * np.random.uniform(0, 0.3, n), 2)
returns_col  = (np.random.rand(n) < 0.08).astype(int)   # 8% return rate
rating_col   = np.round(np.random.uniform(1, 5, n), 1)

df = pd.DataFrame({
    'Month':    month_col,
    'Month_Num':np.vectorize(lambda m: month_num[m])(month_col),
    'Category': cat_col,
    'Region':   region_col,
    'Channel':  channel_col,
    'Gender':   gender_col,
    'Units':    units_col,
    'Revenue':  revenue_col,
    'Discount': discount_col,
    'Returned': returns_col,
    'Rating':   rating_col,
})

# Sort by month number for correct month ordering
df = df.sort_values('Month_Num').reset_index(drop=True)

print(f"\nDataset created: {df.shape[0]:,} transactions × {df.shape[1]} columns")
print(f"Date range:  {df['Month'].unique().tolist()}")
print(f"Categories:  {df['Category'].unique().tolist()}")
print(f"Total Revenue: ₹{df['Revenue'].sum():>15,.0f}")
print()
print(df.head(8).to_string())

# ============================================================
print("\n" + "=" * 70)
print("  SECTION 3: BASIC PIVOT TABLE")
print("=" * 70)

# ── 3A. Basic: Month × Category Revenue ──────────────────────
month_order = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']

pivot_basic = pd.pivot_table(
    df,
    values    = 'Revenue',
    index     = 'Month',
    columns   = 'Category',
    aggfunc   = 'sum',
    fill_value= 0,
)
# Reorder months chronologically
pivot_basic = pivot_basic.reindex(month_order)

print("\n[3A] Basic Pivot — Total Revenue by Month × Category:")
print(pivot_basic.round(0).to_string())

# ── 3B. With margins=True ─────────────────────────────────────
print("\n[3B] With margins=True — adds Grand Total row and column:")
pivot_margins = pd.pivot_table(
    df,
    values       = 'Revenue',
    index        = 'Month',
    columns      = 'Category',
    aggfunc      = 'sum',
    fill_value   = 0,
    margins      = True,
    margins_name = '📊 Grand Total',
)
pivot_margins = pivot_margins.reindex(month_order + ['📊 Grand Total'])
print(pivot_margins.round(0).to_string())

# ── 3C. Different aggfunc — average ──────────────────────────
print("\n[3C] aggfunc='mean' — Average Revenue per Transaction:")
pivot_mean = pd.pivot_table(
    df,
    values    = 'Revenue',
    index     = 'Month',
    columns   = 'Category',
    aggfunc   = 'mean',
    fill_value= 0,
)
pivot_mean = pivot_mean.reindex(month_order)
print(pivot_mean.round(1).to_string())

# ── 3D. aggfunc='count' ───────────────────────────────────────
print("\n[3D] aggfunc='count' — Number of Transactions:")
pivot_count = pd.pivot_table(
    df,
    values    = 'Revenue',
    index     = 'Month',
    columns   = 'Category',
    aggfunc   = 'count',
    fill_value= 0,
)
pivot_count = pivot_count.reindex(month_order)
print(pivot_count.to_string())

# ============================================================
print("\n" + "=" * 70)
print("  SECTION 4: MULTI-DIMENSIONAL PIVOTS")
print("=" * 70)

# ── 4A. MultiIndex index (Region + Month) ────────────────────
print("\n[4A] Multi-level index — Region + Month as rows:")
pivot_multi_idx = pd.pivot_table(
    df,
    values    = 'Revenue',
    index     = ['Region', 'Month'],
    columns   = 'Category',
    aggfunc   = 'sum',
    fill_value= 0,
)
print(pivot_multi_idx.round(0).head(12).to_string())

# ── 4B. Multiple values — Revenue AND Units ───────────────────
print("\n[4B] Multiple values — Revenue AND Units in same pivot:")
pivot_multi_val = pd.pivot_table(
    df,
    values    = ['Revenue', 'Units'],
    index     = 'Month',
    columns   = 'Category',
    aggfunc   = 'sum',
    fill_value= 0,
)
pivot_multi_val = pivot_multi_val.reindex(month_order)
print(pivot_multi_val.round(0).head(6).to_string())
print("  ↑ MultiIndex COLUMNS: outer level = metric, inner = category")

# ── 4C. Multiple aggfuncs ─────────────────────────────────────
print("\n[4C] Multiple aggfuncs — sum + mean + count in one pivot:")
pivot_multi_agg = pd.pivot_table(
    df,
    values    = 'Revenue',
    index     = 'Region',
    columns   = 'Channel',
    aggfunc   = {'Revenue': ['sum', 'mean', 'count']},
    fill_value= 0,
)
print(pivot_multi_agg.round(1).to_string())

# ── 4D. Region × Channel → Revenue (with margins) ────────────
print("\n[4D] Region × Channel Pivot (with Grand Total):")
pivot_region_channel = pd.pivot_table(
    df,
    values       = 'Revenue',
    index        = 'Region',
    columns      = 'Channel',
    aggfunc      = 'sum',
    margins      = True,
    margins_name = 'Total',
    fill_value   = 0,
)
print(pivot_region_channel.round(0).to_string())

# ── 4E. Customer Rating pivot ─────────────────────────────────
print("\n[4E] Average Rating by Category × Channel:")
pivot_rating = pd.pivot_table(
    df,
    values    = 'Rating',
    index     = 'Category',
    columns   = 'Channel',
    aggfunc   = 'mean',
    fill_value= 0,
    margins   = True,
    margins_name='All Channels',
)
print(pivot_rating.round(2).to_string())

# ── 4F. Return rate pivot ─────────────────────────────────────
print("\n[4F] Return Rate (%) by Category × Region:")
pivot_returns = pd.pivot_table(
    df,
    values    = 'Returned',
    index     = 'Category',
    columns   = 'Region',
    aggfunc   = 'mean',          # mean of 0/1 = proportion
    fill_value= 0,
) * 100   # convert to percentage
print(pivot_returns.round(1).to_string())
print("  Values = Return Rate % (higher = more returns)")


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 5: INSIGHTS FROM PIVOT")
print("=" * 70)

# Find best month per category
print("\n[5A] Best Month per Category (highest revenue):")
for cat in categories:
    best_month = pivot_basic[cat].idxmax()
    best_rev   = pivot_basic[cat].max()
    print(f"  {cat:<18s}: {best_month}  ₹{best_rev:>12,.0f}")

# Find best category per month
print("\n[5B] Best Category per Month:")
for month in month_order:
    best_cat = pivot_basic.loc[month].idxmax()
    best_rev = pivot_basic.loc[month].max()
    print(f"  {month}: {best_cat:<18s}  ₹{best_rev:>10,.0f}")


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 6: VISUALIZATIONS")
print("=" * 70)

# ─────────────────────────────────────────────────────────────
# CHART 1: Revenue Heatmap — Month × Category
# ─────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(14, 7))
fig1.patch.set_facecolor('#0D1117')
ax1.set_facecolor('#0D1117')

# Custom colormap: dark blue → teal → gold
colors_hm = ['#0D1B2A', '#1B4F72', '#2E86AB', '#A23B72', '#F18F01', '#FFD60A']
cmap_custom = LinearSegmentedColormap.from_list('techmap', colors_hm, N=256)

data_hm = pivot_basic.values
im = ax1.imshow(data_hm, cmap=cmap_custom, aspect='auto', interpolation='nearest')

# Axes
ax1.set_xticks(range(len(categories)))
ax1.set_xticklabels(categories, color='#E0E0E0', fontsize=10, rotation=25, ha='right')
ax1.set_yticks(range(len(month_order)))
ax1.set_yticklabels(month_order, color='#E0E0E0', fontsize=10)

# Annotate cells
for i in range(len(month_order)):
    for j in range(len(categories)):
        val = data_hm[i, j]
        text_color = 'white' if val < data_hm.max() * 0.6 else '#0D1117'
        ax1.text(j, i, f'₹{val/1000:.0f}K', ha='center', va='center',
                 color=text_color, fontsize=8.5, fontweight='bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax1, fraction=0.03, pad=0.02)
cbar.ax.tick_params(colors='#A0A0A0')
cbar.set_label('Revenue (₹)', color='#A0A0A0', fontsize=10)

# Labels + title
ax1.set_title('📊 E-Commerce Revenue Heatmap — Month × Category',
              color='white', fontsize=14, fontweight='bold', pad=16)
ax1.set_xlabel('Product Category', color='#A0A0A0', fontsize=11, labelpad=10)
ax1.set_ylabel('Month', color='#A0A0A0', fontsize=11, labelpad=10)

# Grid lines between cells
ax1.set_xticks(np.arange(-.5, len(categories), 1), minor=True)
ax1.set_yticks(np.arange(-.5, len(month_order), 1), minor=True)
ax1.grid(which='minor', color='#1E1E2E', linewidth=1.5)
ax1.tick_params(which='minor', bottom=False, left=False)

plt.tight_layout()
fig1.savefig('/home/claude/day14/chart1_revenue_heatmap.png', dpi=150,
             bbox_inches='tight', facecolor='#0D1117')
plt.close(fig1)
print("\n[6A] ✅ Chart 1 saved: Revenue Heatmap (Month × Category)")

# ─────────────────────────────────────────────────────────────
# CHART 2: Stacked Bar — Monthly Revenue by Category
# ─────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(14, 6))
fig2.patch.set_facecolor('#0D1117')
ax2.set_facecolor('#0D1117')

colors_bar = ['#2E86AB', '#A23B72', '#F18F01', '#44BBA4', '#E94F37', '#B8B8FF']
bottom = np.zeros(len(month_order))

for i, cat in enumerate(categories):
    vals = pivot_basic[cat].values
    bars = ax2.bar(month_order, vals, bottom=bottom, color=colors_bar[i],
                   label=cat, alpha=0.9, width=0.75, edgecolor='#0D1117', linewidth=0.5)
    bottom += vals

# Style
ax2.set_facecolor('#0D1117')
ax2.tick_params(colors='#A0A0A0', labelsize=10)
ax2.set_xlabel('Month', color='#A0A0A0', fontsize=11, labelpad=8)
ax2.set_ylabel('Revenue (₹)', color='#A0A0A0', fontsize=11, labelpad=8)
ax2.set_title('📈 Monthly Revenue by Product Category (Stacked)',
              color='white', fontsize=14, fontweight='bold', pad=14)

# Format y-axis as ₹K
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))

legend = ax2.legend(loc='upper left', framealpha=0.3, facecolor='#1A1A2E',
                    edgecolor='#444', labelcolor='white', fontsize=9)

for spine in ax2.spines.values():
    spine.set_edgecolor('#333')

ax2.grid(axis='y', color='#2A2A3A', alpha=0.5, linewidth=0.7)
ax2.set_axisbelow(True)

plt.tight_layout()
fig2.savefig('/home/claude/day14/chart2_stacked_bar.png', dpi=150,
             bbox_inches='tight', facecolor='#0D1117')
plt.close(fig2)
print("[6B] ✅ Chart 2 saved: Stacked Bar (Monthly Revenue by Category)")

# ─────────────────────────────────────────────────────────────
# CHART 3: Channel × Region Revenue Heatmap
# ─────────────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(8, 5))
fig3.patch.set_facecolor('#0D1117')
ax3.set_facecolor('#0D1117')

pivot_ch_reg = pd.pivot_table(
    df, values='Revenue', index='Region', columns='Channel',
    aggfunc='sum', fill_value=0
)
data_cr = pivot_ch_reg.values
channels_list = pivot_ch_reg.columns.tolist()
regions_list  = pivot_ch_reg.index.tolist()

colors_cr = ['#0D1B2A', '#1B4F72', '#148F77', '#D4AC0D', '#E74C3C']
cmap_cr   = LinearSegmentedColormap.from_list('chanreg', colors_cr, N=256)

im3 = ax3.imshow(data_cr, cmap=cmap_cr, aspect='auto')

ax3.set_xticks(range(len(channels_list)))
ax3.set_xticklabels(channels_list, color='#E0E0E0', fontsize=11)
ax3.set_yticks(range(len(regions_list)))
ax3.set_yticklabels(regions_list, color='#E0E0E0', fontsize=11)

for i in range(len(regions_list)):
    for j in range(len(channels_list)):
        val = data_cr[i, j]
        tc  = 'white' if val < data_cr.max() * 0.55 else '#111'
        ax3.text(j, i, f'₹{val/1000:.0f}K', ha='center', va='center',
                 color=tc, fontsize=11, fontweight='bold')

cbar3 = plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)
cbar3.ax.tick_params(colors='#A0A0A0')

ax3.set_title('Channel × Region Revenue Matrix',
              color='white', fontsize=13, fontweight='bold', pad=12)
ax3.set_xlabel('Sales Channel', color='#A0A0A0', fontsize=10)
ax3.set_ylabel('Region', color='#A0A0A0', fontsize=10)

ax3.set_xticks(np.arange(-.5, len(channels_list), 1), minor=True)
ax3.set_yticks(np.arange(-.5, len(regions_list), 1), minor=True)
ax3.grid(which='minor', color='#1E1E2E', linewidth=2)
ax3.tick_params(which='minor', bottom=False, left=False)

plt.tight_layout()
fig3.savefig('/home/claude/day14/chart3_channel_region.png', dpi=150,
             bbox_inches='tight', facecolor='#0D1117')
plt.close(fig3)
print("[6C] ✅ Chart 3 saved: Channel × Region Heatmap")

# ─────────────────────────────────────────────────────────────
# CHART 4: Monthly trend lines per category
# ─────────────────────────────────────────────────────────────
fig4, ax4 = plt.subplots(figsize=(14, 6))
fig4.patch.set_facecolor('#0D1117')
ax4.set_facecolor('#0D1117')

x = np.arange(len(month_order))
for i, cat in enumerate(categories):
    vals = pivot_basic[cat].values
    ax4.plot(x, vals, color=colors_bar[i], marker='o', linewidth=2.5,
             markersize=6, label=cat, alpha=0.9)
    # Shade Nov + Dec (seasonal peak)
ax4.axvspan(10, 11, alpha=0.1, color='#FFD60A', label='Festive Season')

ax4.set_xticks(x)
ax4.set_xticklabels(month_order, color='#A0A0A0', fontsize=10)
ax4.tick_params(axis='y', colors='#A0A0A0')
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'₹{v/1000:.0f}K'))
ax4.set_xlabel('Month', color='#A0A0A0', fontsize=11, labelpad=8)
ax4.set_ylabel('Revenue (₹)', color='#A0A0A0', fontsize=11, labelpad=8)
ax4.set_title('📉 Revenue Trend Lines by Category — Full Year',
              color='white', fontsize=14, fontweight='bold', pad=14)
ax4.legend(loc='upper left', framealpha=0.3, facecolor='#1A1A2E',
           edgecolor='#444', labelcolor='white', fontsize=9)

for spine in ax4.spines.values():
    spine.set_edgecolor('#333')
ax4.grid(color='#2A2A3A', alpha=0.4, linewidth=0.7)

plt.tight_layout()
fig4.savefig('/home/claude/day14/chart4_trend_lines.png', dpi=150,
             bbox_inches='tight', facecolor='#0D1117')
plt.close(fig4)
print("[6D] ✅ Chart 4 saved: Trend Lines (Category Revenue Over Year)")


# ─────────────────────────────────────────────────────────────
# COMBINED FIGURE — All 4 charts as a dashboard
# ─────────────────────────────────────────────────────────────
fig_dash = plt.figure(figsize=(20, 16))
fig_dash.patch.set_facecolor('#0D1117')

# Add super title
fig_dash.suptitle('🛒  E-Commerce Sales Analysis Dashboard — Full Year',
                  color='white', fontsize=18, fontweight='bold', y=0.98)

# ── Subplot 1: Heatmap ────────────────────────────────────────
ax_h = fig_dash.add_subplot(2, 2, 1)
ax_h.set_facecolor('#0D1117')
im_h = ax_h.imshow(data_hm, cmap=cmap_custom, aspect='auto')
ax_h.set_xticks(range(len(categories)))
ax_h.set_xticklabels(categories, color='#CCC', fontsize=7.5, rotation=30, ha='right')
ax_h.set_yticks(range(len(month_order)))
ax_h.set_yticklabels(month_order, color='#CCC', fontsize=8)
for i in range(len(month_order)):
    for j in range(len(categories)):
        v  = data_hm[i, j]
        tc = 'white' if v < data_hm.max() * 0.6 else '#0D1117'
        ax_h.text(j, i, f'₹{v/1000:.0f}K', ha='center', va='center',
                  color=tc, fontsize=6.5, fontweight='bold')
ax_h.set_title('Revenue Heatmap', color='white', fontsize=11, fontweight='bold')
ax_h.set_xticks(np.arange(-.5, len(categories), 1), minor=True)
ax_h.set_yticks(np.arange(-.5, len(month_order), 1), minor=True)
ax_h.grid(which='minor', color='#1E1E2E', linewidth=1)
ax_h.tick_params(which='minor', bottom=False, left=False)

# ── Subplot 2: Stacked Bar ────────────────────────────────────
ax_b = fig_dash.add_subplot(2, 2, 2)
ax_b.set_facecolor('#0D1117')
bot = np.zeros(len(month_order))
for i, cat in enumerate(categories):
    vals = pivot_basic[cat].values
    ax_b.bar(month_order, vals, bottom=bot, color=colors_bar[i],
             label=cat, alpha=0.9, width=0.78, edgecolor='#0D1117', linewidth=0.4)
    bot += vals
ax_b.tick_params(colors='#AAA', labelsize=8)
ax_b.set_xticklabels(month_order, rotation=45, ha='right', color='#AAA', fontsize=7)
ax_b.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'₹{v/1000:.0f}K'))
ax_b.legend(fontsize=7, framealpha=0.3, facecolor='#1A1A2E',
            edgecolor='#444', labelcolor='white', loc='upper left')
ax_b.set_title('Stacked Monthly Revenue', color='white', fontsize=11, fontweight='bold')
ax_b.grid(axis='y', color='#2A2A3A', alpha=0.4)
for spine in ax_b.spines.values(): spine.set_edgecolor('#333')

# ── Subplot 3: Channel × Region ──────────────────────────────
ax_c = fig_dash.add_subplot(2, 2, 3)
ax_c.set_facecolor('#0D1117')
im_c = ax_c.imshow(data_cr, cmap=cmap_cr, aspect='auto')
ax_c.set_xticks(range(len(channels_list)))
ax_c.set_xticklabels(channels_list, color='#CCC', fontsize=9)
ax_c.set_yticks(range(len(regions_list)))
ax_c.set_yticklabels(regions_list, color='#CCC', fontsize=9)
for i in range(len(regions_list)):
    for j in range(len(channels_list)):
        v  = data_cr[i, j]
        tc = 'white' if v < data_cr.max() * 0.55 else '#111'
        ax_c.text(j, i, f'₹{v/1000:.0f}K', ha='center', va='center',
                  color=tc, fontsize=9, fontweight='bold')
ax_c.set_title('Channel × Region Matrix', color='white', fontsize=11, fontweight='bold')
ax_c.set_xticks(np.arange(-.5, len(channels_list), 1), minor=True)
ax_c.set_yticks(np.arange(-.5, len(regions_list), 1), minor=True)
ax_c.grid(which='minor', color='#1E1E2E', linewidth=2)
ax_c.tick_params(which='minor', bottom=False, left=False)

# ── Subplot 4: Trend Lines ────────────────────────────────────
ax_t = fig_dash.add_subplot(2, 2, 4)
ax_t.set_facecolor('#0D1117')
for i, cat in enumerate(categories):
    vals = pivot_basic[cat].values
    ax_t.plot(x, vals, color=colors_bar[i], marker='o', linewidth=2,
              markersize=4, label=cat, alpha=0.9)
ax_t.axvspan(10, 11, alpha=0.1, color='#FFD60A')
ax_t.set_xticks(x)
ax_t.set_xticklabels(month_order, color='#AAA', fontsize=7.5, rotation=45, ha='right')
ax_t.tick_params(axis='y', colors='#AAA', labelsize=8)
ax_t.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'₹{v/1000:.0f}K'))
ax_t.legend(fontsize=7, framealpha=0.3, facecolor='#1A1A2E',
            edgecolor='#444', labelcolor='white')
ax_t.set_title('Revenue Trend Lines', color='white', fontsize=11, fontweight='bold')
ax_t.grid(color='#2A2A3A', alpha=0.4)
for spine in ax_t.spines.values(): spine.set_edgecolor('#333')

plt.tight_layout(rect=[0, 0, 1, 0.96])
fig_dash.savefig('/home/claude/day14/dashboard_combined.png', dpi=150,
                bbox_inches='tight', facecolor='#0D1117')
plt.close(fig_dash)
print("[6E] ✅ Dashboard saved: All 4 charts combined!")


# ============================================================
print("\n" + "=" * 70)
print("  SECTION 7: KEY PIVOT INSIGHTS")
print("=" * 70)

total = df['Revenue'].sum()
print(f"\n📦 Total Revenue:     ₹{total:>15,.0f}")
print(f"📋 Total Transactions: {len(df):>14,}")
print(f"📊 Avg Order Value:   ₹{total/len(df):>14,.0f}")
print(f"↩️  Overall Return Rate: {df['Returned'].mean()*100:.1f}%")

print("\n🏆 Category Rankings by Total Revenue:")
cat_totals = pivot_margins[categories].loc['📊 Grand Total'].sort_values(ascending=False)
for rank, (cat, rev) in enumerate(cat_totals.items(), 1):
    pct = rev / total * 100
    bar = '█' * int(pct // 2)
    print(f"  {rank}. {cat:<18s}  ₹{rev:>12,.0f}  ({pct:4.1f}%)  {bar}")

print("\n📅 Seasonal Insights:")
q4_months = ['Oct', 'Nov', 'Dec']
q4_rev    = pivot_basic.loc[q4_months].sum().sum()
print(f"  Q4 (Oct-Dec) Revenue: ₹{q4_rev:>12,.0f}  ({q4_rev/total*100:.1f}% of annual)")
print(f"  Nov + Dec alone:      ₹{pivot_margins[categories].loc[['Nov','Dec']].sum().sum():>12,.0f}")

print("\n🌍 Regional Split:")
reg_pivot = pd.pivot_table(df, values='Revenue', index='Region', aggfunc='sum').sort_values('Revenue', ascending=False)
for r, row in reg_pivot.iterrows():
    print(f"  {r:8s}: ₹{row['Revenue']:>12,.0f}  ({row['Revenue']/total*100:.1f}%)")

print()
print("=" * 70)
print("  FILES SAVED:")
print("  📊 chart1_revenue_heatmap.png   — Month × Category heatmap")
print("  📊 chart2_stacked_bar.png        — Stacked monthly bars")
print("  📊 chart3_channel_region.png     — Channel × Region matrix")
print("  📊 chart4_trend_lines.png        — Revenue trends by category")
print("  📊 dashboard_combined.png        — All 4 charts as dashboard")
print("=" * 70)
print("\n✅ pivot_project.py complete!")
