import pandas as pd
from sqlalchemy import create_engine

# Read cleaned CSV
df = pd.read_csv("customer_shopping_behavior_cleaned.csv")

# PostgreSQL connection
engine = create_engine(
    "postgresql://postgres:zig@localhost:5432/customer_behavior"
)

# Send dataframe to PostgreSQL
df.to_sql(
    "customer_shopping",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Data imported successfully!")