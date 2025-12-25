"""
Preprocessing script for referral data.

This script uses user_referrals as the base table and joins
all related source tables to create a clean dataset for
downstream business logic.
"""

import pandas as pd
from pathlib import Path
import numpy as np

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

# base table
referrals_df = dfs["user_referrals"].copy()

# join referral status
status_df = dfs["user_referral_statuses"][["id", "description"]].copy()

referrals_df = referrals_df.merge(
    status_df,
    left_on="user_referral_status_id",
    right_on="id",
    how="left"
)

referrals_df = referrals_df.rename(
    columns={"description": "referral_status"}
)

referrals_df = referrals_df.drop(columns=["id"])

print(referrals_df["referral_status"].value_counts())

# join referral rewards
rewards_df = dfs["referral_rewards"].copy()
rewards_df = rewards_df.rename(columns={"id": "reward_id"})

referrals_df = referrals_df.merge(
    rewards_df,
    left_on="referral_reward_id",
    right_on="reward_id",
    how="left"
)

referrals_df = referrals_df.drop(columns=["reward_id"])

# join paid transactions
transactions_df = dfs["paid_transactions"].copy()

referrals_df = referrals_df.merge(
    transactions_df,
    on="transaction_id",
    how="left"
)

# prepare unique user logs
user_logs_unique = (
    dfs["user_logs"]
    .drop_duplicates(subset=["user_id"], keep="last")
)

# join referrer user info
referrer_df = user_logs_unique.copy()

referrer_df = referrer_df.rename(columns={
    "user_id": "referrer_id",
    "name": "referrer_name",
    "phone_number": "referrer_phone_number",
    "homeclub": "referrer_homeclub",
    "timezone_homeclub": "referrer_timezone",
    "membership_expired_date": "referrer_membership_expired_date",
    "is_deleted": "referrer_is_deleted"
})

referrals_df = referrals_df.merge(
    referrer_df,
    on="referrer_id",
    how="left"
)

# join referee user info
referee_df = user_logs_unique.copy()

referee_df = referee_df.rename(columns={
    "user_id": "referee_id",
    "name": "referee_name_user",
    "phone_number": "referee_phone_user"
})

referrals_df = referrals_df.merge(
    referee_df[["referee_id", "referee_name_user", "referee_phone_user"]],
    on="referee_id",
    how="left"
)

# prepare unique lead logs
lead_logs_unique = (
    dfs["lead_logs"]
    .sort_values("created_at")
    .drop_duplicates(subset=["lead_id"], keep="last")
)

# join lead logs
referrals_df = referrals_df.merge(
    lead_logs_unique,
    left_on="referee_id",
    right_on="lead_id",
    how="left",
    suffixes=("", "_lead")
)

# parse datetime columns

time_cols = [
    "referral_at",
    "updated_at",
    "transaction_at",
    "created_at"
]

for col in time_cols:
    if col in referrals_df.columns:
        referrals_df[col] = pd.to_datetime(referrals_df[col], errors="coerce")
# convert referral time to referrer local timezone 
if "referrer_timezone" in referrals_df.columns and "referral_at" in referrals_df.columns:
    if referrals_df["referral_at"].dt.tz is None:
        referrals_df["referral_at_local"] = (
            referrals_df["referral_at"]
            .dt.tz_localize("UTC", nonexistent="NaT", ambiguous="NaT")
            .dt.tz_convert(referrals_df["referrer_timezone"].iloc[0])
        )
    else:
        referrals_df["referral_at_local"] = (
            referrals_df["referral_at"]
            .dt.tz_convert(referrals_df["referrer_timezone"].iloc[0])
        )


referrals_df["referral_source_category"] = np.where(
    referrals_df["referral_source"] == "User Sign Up",
    "Online",
    np.where(
        referrals_df["referral_source"] == "Draft Transaction",
        "Offline",
        referrals_df["source_category"]
    )
)

print("Final shape after preprocessing:", referrals_df.shape)

referrals_df.to_csv(
    "preprocessed_referrals.csv",
    index=False
)

print("Preprocessing completed.")
