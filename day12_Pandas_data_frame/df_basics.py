# ============================================================
# DAY 12 — PANDAS DataFrames: BASICS + FILTERING
# Dataset: Titanic (Kaggle)
# Download: https://www.kaggle.com/datasets/yasserh/titanic-dataset
# Save as: titanic.csv in same folder
# ============================================================

import pandas as pd
import numpy as np

print("=" * 60)
print("SECTION 1: DATAFRAME CREATION")
print("=" * 60)

# ── 1A. From a Python List (of dicts) ──────────────────────
data_list = [
    {"Name": "Alice", "Age": 24, "Score": 88},
    {"Name": "Bob",   "Age": 27, "Score": 72},
    {"Name": "Carol", "Age": 22, "Score": 95},
]
df_list = pd.DataFrame(data_list)
print("\n[1A] DataFrame from list of dicts:")
print(df_list)

# ── 1B. From a Dictionary ──────────────────────────────────
data_dict = {
    "Name":  ["Alice", "Bob", "Carol"],
    "Age":   [24, 27, 22],
    "Score": [88, 72, 95],
}
df_dict = pd.DataFrame(data_dict)
print("\n[1B] DataFrame from dict:")
print(df_dict)

# ── 1C. From CSV (Titanic dataset) ─────────────────────────
# Make sure titanic.csv is in the same directory
try:
    df = pd.read_csv("titanic.csv")
    print("\n[1C] Titanic CSV loaded. Shape:", df.shape)
except FileNotFoundError:
    print("\n[1C] titanic.csv not found! Using sample data instead.")
    # Fallback mini-dataset that mirrors Titanic columns
    df = pd.DataFrame({
        "PassengerId": [1, 2, 3, 4, 5],
        "Survived":    [0, 1, 1, 0, 1],
        "Pclass":      [3, 1, 3, 1, 2],
        "Name":        ["Braund, Mr. Owen", "Cumings, Mrs. John", "Heikkinen, Miss. Laina",
                        "Futrelle, Mrs. Jacques", "Allen, Mr. William"],
        "Sex":         ["male", "female", "female", "female", "male"],
        "Age":         [22.0, 38.0, np.nan, 35.0, 35.0],
        "SibSp":       [1, 1, 0, 1, 0],
        "Parch":       [0, 0, 0, 0, 0],
        "Ticket":      ["A/5 21171", "PC 17599", "STON/O2", "113803", "373450"],
        "Fare":        [7.25, 71.28, 7.92, 53.10, 8.05],
        "Cabin":       [np.nan, "C85", np.nan, "C123", np.nan],
        "Embarked":    ["S", "C", "S", "S", "S"],
    })
    print("[1C] Fallback mini-Titanic dataset created.")

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 2: DATAFRAME ATTRIBUTES")
print("=" * 60)

print("\n[2.1] df.shape       →", df.shape)           # (rows, cols)
print("[2.2] df.ndim        →", df.ndim)              # always 2 for DataFrame
print("[2.3] df.size        →", df.size)              # total cells
print("\n[2.4] df.dtypes:\n",    df.dtypes)
print("\n[2.5] df.columns    →", df.columns.tolist())
print("[2.6] df.index      →", df.index)

print("\n[2.7] df.head(3):")
print(df.head(3))

print("\n[2.8] df.tail(3):")
print(df.tail(3))

print("\n[2.9] df.sample(2) — random 2 rows:")
print(df.sample(2, random_state=42))

print("\n[2.10] df.info():")
df.info()

print("\n[2.11] df.describe():")
print(df.describe())

print("\n[2.12] df.describe(include='all') — includes object columns:")
print(df.describe(include="all"))

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 3: NULL & DUPLICATE DETECTION")
print("=" * 60)

print("\n[3.1] df.isnull().sum() — NaN count per column:")
print(df.isnull().sum())

print("\n[3.2] df.isnull().sum().sum() — Total NaNs:", df.isnull().sum().sum())

print("\n[3.3] df.duplicated().sum() — Duplicate rows:", df.duplicated().sum())

print("\n[3.4] df.hasnans — does ANY column have NaN? ",)
for col in df.columns:
    print(f"       {col}: {df[col].hasnans}")

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 4: RENAME COLUMNS")
print("=" * 60)

# Rename using a dict — only columns listed get renamed
df_renamed = df.rename(columns={"Pclass": "PassengerClass", "SibSp": "Siblings_Spouses"})
print("[4.1] Renamed columns:", df_renamed.columns.tolist())

# Rename using a function (lowercase all)
df_lower = df.rename(columns=str.lower)
print("[4.2] All lowercase:", df_lower.columns.tolist())

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 5: MATHS ON DATAFRAME (sum/mean/var with axis)")
print("=" * 60)

# axis=0 → column-wise (default), axis=1 → row-wise
numeric_cols = df.select_dtypes(include="number")

print("\n[5.1] Column-wise SUM (axis=0):")
print(numeric_cols.sum(axis=0))

print("\n[5.2] Row-wise SUM (axis=1) — first 5 rows:")
print(numeric_cols.sum(axis=1).head())

print("\n[5.3] Column-wise MEAN:")
print(numeric_cols.mean(axis=0))

print("\n[5.4] Column-wise VARIANCE:")
print(numeric_cols.var(axis=0))

print("\n[5.5] Column-wise STD:")
print(numeric_cols.std(axis=0))

print("\n[5.6] Min / Max:")
print("Min:\n", numeric_cols.min())
print("Max:\n", numeric_cols.max())

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 6: ROW / COLUMN SELECTION")
print("=" * 60)

# ── Single column → returns Series ──────────────────────────
print("\n[6.1] Single column (Series):")
print(df["Age"].head())

# ── Multiple columns → returns DataFrame ───────────────────
print("\n[6.2] Multiple columns (DataFrame):")
print(df[["Name", "Survived", "Age"]].head())

# ── iloc — position-based ───────────────────────────────────
print("\n[6.3] iloc[0] — first row (Series):")
print(df.iloc[0])

print("\n[6.4] iloc[0:3] — rows 0,1,2:")
print(df.iloc[0:3])

print("\n[6.5] iloc[0:3, 0:4] — rows 0-2, cols 0-3:")
print(df.iloc[0:3, 0:4])

print("\n[6.6] iloc[[0, 2, 4], [1, 3]] — specific rows & cols:")
print(df.iloc[[0, 2, 4], [1, 3]])

# ── loc — label-based ───────────────────────────────────────
print("\n[6.7] loc[0, 'Name'] — single cell:")
print(df.loc[0, "Name"])

print("\n[6.8] loc[0:2, ['Name','Age','Survived']]:")
print(df.loc[0:2, ["Name", "Age", "Survived"]])

print("\n")

# ============================================================
print("=" * 60)
print("SECTION 7: FILTERING (Boolean Masking)")
print("=" * 60)

# ── Single condition ────────────────────────────────────────
survived = df[df["Survived"] == 1]
print(f"\n[7.1] Survivors: {len(survived)} rows")
print(survived[["Name", "Age", "Pclass"]].head(3))

# ── AND condition (&) ───────────────────────────────────────
rich_survivors = df[(df["Survived"] == 1) & (df["Pclass"] == 1)]
print(f"\n[7.2] 1st class survivors: {len(rich_survivors)} rows")
print(rich_survivors[["Name", "Age", "Fare"]].head(3))

# ── OR condition (|) ────────────────────────────────────────
young_or_1st = df[(df["Age"] < 18) | (df["Pclass"] == 1)]
print(f"\n[7.3] Under-18 OR 1st class: {len(young_or_1st)} rows")

# ── str.contains ────────────────────────────────────────────
miss_filter = df[df["Name"].str.contains("Miss", na=False)]
print(f"\n[7.4] Passengers with 'Miss' in name: {len(miss_filter)}")
print(miss_filter[["Name", "Age", "Survived"]].head(3))

# ── Add a new column ────────────────────────────────────────
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
print("\n[7.5] New column 'FamilySize' added:")
print(df[["Name", "SibSp", "Parch", "FamilySize"]].head(4))

# ── astype — change dtype ───────────────────────────────────
df["Survived_str"] = df["Survived"].astype(str)
print("\n[7.6] astype: Survived as string:", df["Survived_str"].dtype)

# ── value_counts ────────────────────────────────────────────
print("\n[7.7] value_counts on 'Pclass':")
print(df["Pclass"].value_counts())

print("\n[7.8] value_counts(normalize=True) — proportions:")
print(df["Pclass"].value_counts(normalize=True).round(2))

# ── sort_values (basic) ─────────────────────────────────────
print("\n[7.9] sort_values by Age (ascending):")
print(df[["Name", "Age"]].sort_values("Age").head(4))

print("\n[7.10] sort_values by Age (descending):")
print(df[["Name", "Age"]].sort_values("Age", ascending=False).head(4))

print("\n[7.11] sort_values by multiple columns (Pclass asc, Fare desc):")
print(df[["Name", "Pclass", "Fare"]].sort_values(["Pclass", "Fare"], ascending=[True, False]).head(5))

print("\n")
print("✅ df_basics.py complete!")
