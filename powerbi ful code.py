# ==========================================================
# Customer Shopping Behavior Dataset - Data Cleaning & SQL Export
# ==========================================================

# Import libraries
import pandas as pd

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv("customer_shop.csv")

# Display first five rows
print(df.head())

# Dataset information
print(df.info())

# Summary statistics
print(df.describe(include="all"))

# ==========================================================
# Check Missing Values
# ==========================================================

print("\nMissing Values:")
print(df.isnull().sum())

# ==========================================================
# Fill Missing Review Ratings
# ==========================================================

df["Review Rating"] = (
    df.groupby("Category")["Review Rating"]
    .transform(lambda x: x.fillna(x.median()))
)

print("\nMissing Values After Imputation:")
print(df.isnull().sum())

# ==========================================================
# Rename Columns
# ==========================================================

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")
df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})

print("\nColumn Names:")
print(df.columns)

# ==========================================================
# Create Age Group
# ==========================================================

labels = [
    "Young Adult",
    "Adult",
    "Middle-aged",
    "Senior"
]

df["age_group"] = pd.qcut(
    df["age"],
    q=4,
    labels=labels
)

print(df[["age", "age_group"]].head())

# ==========================================================
# Create Purchase Frequency in Days
# ==========================================================

frequency_mapping = {
    "Fortnightly": 14,
    "Weekly": 7,
    "Monthly": 30,
    "Quarterly": 90,
    "Bi-Weekly": 14,
    "Annually": 365,
    "Every 3 Months": 90
}

df["purchase_frequency_days"] = (
    df["frequency_of_purchases"]
    .map(frequency_mapping)
)

print(
    df[
        ["frequency_of_purchases", "purchase_frequency_days"]
    ].head()
)

# ==========================================================
# Check Duplicate Columns
# ==========================================================

print(df[["discount_applied", "promo_code_used"]].head())

print(
    "\nAre both columns identical?",
    (df["discount_applied"] == df["promo_code_used"]).all()
)

# ==========================================================
# Drop Promo Code Used
# ==========================================================

df = df.drop("promo_code_used", axis=1)

print("\nFinal Columns:")
print(df.columns)

# ==========================================================
# Save Cleaned Dataset
# ==========================================================

df.to_csv("customer_shopping_behavior_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully.")

# ==========================================================
# PostgreSQL Export
# ==========================================================

"""
Install:

pip install sqlalchemy psycopg2-binary
"""

from sqlalchemy import create_engine

username = "postgres"
password = "amlan123"      # Change this
host = "localhost"
port = "5432"
database = "customer_behavior"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

table_name = "customer"

df.to_sql(
    table_name,
    engine,
    if_exists="replace",
    index=False
)

print(f"\nData loaded successfully into PostgreSQL table '{table_name}'.")

# ==========================================================
# MySQL Export
# ==========================================================

"""
Install:

pip install sqlalchemy pymysql
"""

from sqlalchemy import create_engine

username = "root"
password = "your_password"
host = "localhost"
port = "3306"
database = "customer_behavior"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

df.to_sql(
    "customer",
    engine,
    if_exists="replace",
    index=False
)

sample = pd.read_sql(
    "SELECT * FROM customer LIMIT 5;",
    engine
)

print(sample)

print("\nData loaded successfully into MySQL.")

# ==========================================================
# SQL Server Export
# ==========================================================

"""
Install:

pip install sqlalchemy pyodbc
"""

from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = "sa"
password = "your_password"
host = "localhost"
port = "1433"
database = "customer_behavior"

driver = quote_plus("ODBC Driver 17 for SQL Server")

engine = create_engine(
    f"mssql+pyodbc://{username}:{password}@{host},{port}/{database}?driver={driver}"
)

df.to_sql(
    "customer",
    engine,
    if_exists="replace",
    index=False
)

sample = pd.read_sql(
    "SELECT TOP 5 * FROM customer;",
    engine
)

print(sample)

print("\nData loaded successfully into SQL Server.")