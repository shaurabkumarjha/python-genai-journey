# ============================================================
# DAY 12 — PANDAS DataFrames: ADVANCED METHODS
# Dataset: Titanic (Kaggle)
# Download: https://www.kaggle.com/datasets/yasserh/titanic-dataset
# Save as: titanic.csv in same folder
# ============================================================

import pandas as pd
import numpy as np

# ── Load dataset ────────────────────────────────────────────
try:
    df = pd.read_csv("titanic.csv")
    print("Titanic CSV loaded. Shape:", df.shape)
except FileNotFoundError:
    df = pd.DataFrame({
        "PassengerId": [1, 2, 3, 4, 5, 6, 7],
        "Survived":    [0, 1, 1, 0, 1, 0, 1],
        "Pclass":      [3, 1, 3, 1, 2, 3, 1],
        "Name":        ["Braund, Mr. Owen", "Cumings, Mrs. John", "Heikkinen, Miss. Laina",
                        "Futrelle, Mrs. Jacques", "Allen, Mr. William",
                        "Moran, Mr. James", "McCarthy, Mr. Timothy"],
        "Sex":         ["male", "female", "female", "female", "male", "male", "male"],
        "Age":         [22.0, 38.0, np.nan, 35.0, 35.0, np.nan, 54.0],
        "SibSp":       [1, 1, 0, 1, 0, 0, 0],
        "Parch":       [0, 0, 0, 0, 0, 0, 0],
        "Ticket":      ["A/5 21171", "PC 17599", "STON/O2", "113803", "373450", "330877", "17463"],
        "Fare":        [7.25, 71.28, 7.92, 53.10, 8.05, 8.46, 51.86],
        "Cabin":       [np.nan, "C85", np.nan, "C123", np.nan, np.nan, "E46"],
        "Embarked":    ["S", "C", "S", "S", "S", "Q", "S"],
    })
    print("Fallback mini-Titanic dataset created.")

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 1: ADVANCED SORTING")
print("=" * 60)

# ── sort_values with na_position ────────────────────────────
print("\n[1.1] sort_values(Age) — NaN at last (default):")
print(df[["Name", "Age"]].sort_values("Age", na_position="last").head(6))

print("\n[1.2] sort_values(Age) — NaN at first:")
print(df[["Name", "Age"]].sort_values("Age", na_position="first").head(6))

# ── inplace=True — modifies original df ─────────────────────
df_copy = df.copy()
df_copy.sort_values("Fare", ascending=False, inplace=True)
print("\n[1.3] After inplace sort by Fare (desc):")
print(df_copy[["Name", "Fare"]].head(4))

# ── sort by multiple columns ────────────────────────────────
print("\n[1.4] Sort by Pclass (asc) then Age (desc):")
print(df.sort_values(["Pclass", "Age"], ascending=[True, False])[["Name", "Pclass", "Age"]].head(6))

# ── sort_index ──────────────────────────────────────────────
df_shuffled = df.sample(frac=1, random_state=42)   # shuffle
print("\n[1.5] Shuffled index:", df_shuffled.index.tolist()[:6])
df_sorted_idx = df_shuffled.sort_index()
print("[1.6] After sort_index:", df_sorted_idx.index.tolist()[:6])

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 2: RANK")
print("=" * 60)

df["Fare_rank"] = df["Fare"].rank(ascending=False)   # highest fare → rank 1
print("\n[2.1] Fare ranking (highest = 1):")
print(df[["Name", "Fare", "Fare_rank"]].sort_values("Fare_rank").head(5))

# Different methods: average, min, max, first, dense
df["Age_rank_dense"] = df["Age"].rank(method="dense", na_option="keep")
print("\n[2.2] Age dense rank (NaN kept as NaN):")
print(df[["Name", "Age", "Age_rank_dense"]].head(6))

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 3: SET_INDEX / RESET_INDEX")
print("=" * 60)

df_indexed = df.set_index("PassengerId")
print("\n[3.1] After set_index('PassengerId'):")
print(df_indexed.head(3))
print("Index:", df_indexed.index.tolist())

# Access by label after set_index
print("\n[3.2] loc[1] after set_index (PassengerId=1):")
print(df_indexed.loc[1, ["Name", "Age", "Survived"]])

# reset_index — bring index back as column
df_reset = df_indexed.reset_index()
print("\n[3.3] After reset_index — PassengerId back as column:")
print(df_reset.columns.tolist())

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 4: RENAME")
print("=" * 60)

df_r = df.rename(columns={
    "Pclass":   "PassengerClass",
    "SibSp":    "Siblings",
    "Parch":    "Parents_Children",
})
print("\n[4.1] Renamed columns:", df_r.columns.tolist())

# Rename rows (index labels)
df_ri = df.rename(index={0: "row_zero", 1: "row_one"})
print("[4.2] Renamed index labels:", df_ri.index.tolist()[:4])

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 5: UNIQUE / NUNIQUE / VALUE_COUNTS")
print("=" * 60)

print("\n[5.1] df['Sex'].unique():", df["Sex"].unique())
print("[5.2] df['Pclass'].unique():", df["Pclass"].unique())
print("[5.3] df['Embarked'].nunique() — number of unique values:", df["Embarked"].nunique())

print("\n[5.4] value_counts on Sex:")
print(df["Sex"].value_counts())

print("\n[5.5] value_counts(normalize=True) — percentages:")
print(df["Sex"].value_counts(normalize=True).mul(100).round(1).astype(str) + "%")

print("\n[5.6] value_counts with dropna=False (includes NaN):")
print(df["Embarked"].value_counts(dropna=False))

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 6: NaN HANDLING")
print("=" * 60)

print("\n[6.1] isnull() — True where NaN:")
print(df[["Age", "Cabin", "Embarked"]].isnull().head(4))

print("\n[6.2] notnull() — True where NOT NaN:")
print(df[["Age", "Cabin"]].notnull().head(4))

print("\n[6.3] hasnans per column:")
for col in df.columns:
    print(f"  {col:20s}: hasnans={df[col].hasnans}")

print("\n[6.4] isnull().sum() — NaN count per column:")
print(df.isnull().sum())

# ── dropna ──────────────────────────────────────────────────
df_drop_any = df.dropna()                              # drop row if ANY NaN
df_drop_how = df.dropna(how="all")                    # drop row if ALL NaN
df_drop_sub = df.dropna(subset=["Age", "Embarked"])   # only check these cols
df_drop_thr = df.dropna(thresh=10)                    # keep rows with ≥10 non-NaN

print(f"\n[6.5] Original rows: {len(df)}")
print(f"      After dropna() (any):           {len(df_drop_any)}")
print(f"      After dropna(how='all'):         {len(df_drop_how)}")
print(f"      After dropna(subset=[Age,Emb]):  {len(df_drop_sub)}")
print(f"      After dropna(thresh=10):         {len(df_drop_thr)}")

# ── fillna ──────────────────────────────────────────────────
df_filled = df.copy()
df_filled["Age"] = df_filled["Age"].fillna(df_filled["Age"].median())
print(f"\n[6.6] fillna(median) on Age — NaN count after: {df_filled['Age'].isnull().sum()}")

df_filled["Embarked"] = df_filled["Embarked"].fillna(df_filled["Embarked"].mode()[0])
print(f"[6.7] fillna(mode) on Embarked — NaN count after: {df_filled['Embarked'].isnull().sum()}")

df_filled["Cabin"] = df_filled["Cabin"].fillna("Unknown")
print(f"[6.8] fillna('Unknown') on Cabin — sample: {df_filled['Cabin'].unique()[:4]}")

# Forward fill / back fill
df_ffill = df[["Age"]].ffill()
df_bfill = df[["Age"]].bfill()
print(f"\n[6.9] ffill sample:\n{df_ffill.head(4)}")

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 7: DUPLICATES")
print("=" * 60)

# Create artificial duplicates for demo
df_dup = pd.concat([df, df.iloc[[0, 1]]], ignore_index=True)
print(f"\n[7.1] Rows after concat with duplicates: {len(df_dup)}")

print("\n[7.2] duplicated() — which rows are duplicates:")
print(df_dup.duplicated().tail(4))

print("\n[7.3] duplicated(keep='last') — keep last occurrence:")
print(df_dup.duplicated(keep="last").head(4))

df_no_dup = df_dup.drop_duplicates()
print(f"\n[7.4] After drop_duplicates(): {len(df_no_dup)} rows")

df_sub_dup = df_dup.drop_duplicates(subset=["Name", "Pclass"])
print(f"[7.5] drop_duplicates(subset=['Name','Pclass']): {len(df_sub_dup)} rows")

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 8: DROP ROWS / COLUMNS")
print("=" * 60)

# drop columns
df_drop_col = df.drop(columns=["Ticket", "Cabin"])
print("\n[8.1] After drop(columns=['Ticket','Cabin']):", df_drop_col.columns.tolist())

# drop rows by index label
df_drop_row = df.drop(index=[0, 2])
print(f"[8.2] After drop(index=[0,2]): {len(df_drop_row)} rows, index: {df_drop_row.index.tolist()[:5]}")

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 9: APPLY")
print("=" * 60)

# ── apply on Series (element-wise via lambda) ───────────────
df_filled["Age_group"] = df_filled["Age"].apply(
    lambda x: "Child" if x < 18 else ("Senior" if x >= 60 else "Adult")
)
print("\n[9.1] Age group using apply + lambda:")
print(df_filled[["Name", "Age", "Age_group"]].head(6))

# ── apply on DataFrame (row-wise, axis=1) ───────────────────
df_filled["FamilySize"] = df_filled[["SibSp", "Parch"]].apply(
    lambda row: row["SibSp"] + row["Parch"] + 1, axis=1
)
print("\n[9.2] FamilySize via apply row-wise:")
print(df_filled[["Name", "SibSp", "Parch", "FamilySize"]].head(4))

# ── apply on a column with a named function ─────────────────
def fare_category(f):
    if f < 10:   return "Budget"
    elif f < 50: return "Standard"
    else:         return "Premium"

df_filled["Fare_category"] = df_filled["Fare"].apply(fare_category)
print("\n[9.3] Fare category using named function + apply:")
print(df_filled[["Name", "Fare", "Fare_category"]].head(6))

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 10: ISIN")
print("=" * 60)

# isin — filter where value is in a list
embarked_CS = df[df["Embarked"].isin(["C", "S"])]
print(f"\n[10.1] Passengers from C or S ports: {len(embarked_CS)}")

pclass_1_2 = df[df["Pclass"].isin([1, 2])]
print(f"[10.2] 1st & 2nd class passengers: {len(pclass_1_2)}")

# NOT isin — using ~ (tilde)
not_3rd = df[~df["Pclass"].isin([3])]
print(f"[10.3] Not 3rd class (using ~isin): {len(not_3rd)}")

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 11: CORR — CORRELATION MATRIX")
print("=" * 60)

numeric_df = df_filled.select_dtypes(include="number")
corr_matrix = numeric_df.corr()
print("\n[11.1] Full correlation matrix:")
print(corr_matrix.round(2))

print("\n[11.2] Correlation with 'Survived':")
print(corr_matrix["Survived"].sort_values(ascending=False).round(3))
# Interpretation: Pclass has negative corr (higher class → lower number → more survived)
# Fare has positive corr (paid more → more likely to survive)

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 12: NLARGEST / NSMALLEST")
print("=" * 60)

print("\n[12.1] nlargest(5, 'Fare') — top 5 fares:")
print(df[["Name", "Fare", "Pclass"]].nlargest(5, "Fare"))

print("\n[12.2] nsmallest(5, 'Age') — youngest 5 passengers:")
print(df_filled[["Name", "Age", "Survived"]].nsmallest(5, "Age"))

print("\n[12.3] nlargest(3, 'Fare') among survivors only:")
surv = df_filled[df_filled["Survived"] == 1]
print(surv[["Name", "Fare"]].nlargest(3, "Fare"))

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 13: INSERT")
print("=" * 60)

# insert(position, column_name, values) — inserts at specific column position
df_ins = df_filled.copy()
df_ins.insert(
    loc=1,                                  # position index
    column="Is_Alone",
    value=(df_ins["FamilySize"] == 1).astype(int)
)
print("\n[13.1] After insert('Is_Alone' at position 1):")
print(df_ins[["PassengerId", "Is_Alone", "FamilySize", "Name"]].head(5))
print("Columns order:", df_ins.columns.tolist()[:5])

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 14: COPY")
print("=" * 60)

# Without copy — changes propagate back (view problem)
df_view = df["Age"]          # This is a view, NOT a copy
df_real_copy = df["Age"].copy()   # This is a true independent copy

df_real_copy.fillna(0, inplace=True)
print("\n[14.1] Original df['Age'] NaN count (unchanged):", df["Age"].isnull().sum())
print("[14.2] Copy NaN count after fillna:", df_real_copy.isnull().sum())

# DataFrame copy
df_c = df.copy()
df_c["Survived"] = 999       # won't affect original
print("\n[14.3] Original df['Survived'] unique:", df["Survived"].unique())
print("[14.4] Modified copy df_c['Survived'] unique:", df_c["Survived"].unique())

print("\n")
print("=" * 60)
print("✅ df_advanced.py complete!")
print("=" * 60)
