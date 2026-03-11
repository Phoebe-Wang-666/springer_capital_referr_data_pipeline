"""
Data profiling script for Springer Capital referral program.

This script loads all referral-related CSV tables and performs
basic data profiling, including null counts and distinct counts
for each column, to understand data quality before further processing.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")


tables = {
    "lead_logs": "lead_log.csv",
    "paid_transactions": "paid_transactions.csv",
    "referral_rewards": "referral_rewards.csv",
    "user_logs": "user_logs.csv",
    "user_referral_logs": "user_referral_logs.csv",
    "user_referral_statuses": "user_referral_statuses.csv",
    "user_referrals": "user_referrals.csv",
}

dfs = {}

for table_name, file_name in tables.items():
    file_path = DATA_DIR / file_name
    df = pd.read_csv(file_path)
    dfs[table_name] = df
    print(f"{table_name} loaded, shape = {df.shape}")

# collect profiling results
profiling_rows = []

for table_name, df in dfs.items():
    for col in df.columns:
        profiling_rows.append({
            "table_name": table_name,
            "column_name": col,
            "null_count": df[col].isna().sum(),
            "distinct_count": df[col].nunique(dropna=True)
        })

# convert results to DataFrame
profiling_df = pd.DataFrame(profiling_rows)

# save profiling output
profiling_df.to_csv("output/profiling_summary.csv", index=False)

print("Data profiling completed.")
print(profiling_df.head())

