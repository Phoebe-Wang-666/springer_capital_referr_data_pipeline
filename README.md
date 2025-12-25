# springer-capital-referral-data-pipeline

A Python-based data pipeline for profiling, preprocessing, and validating referral data, built as part of the Springer Capital internship program.

This project focuses on understanding referral data quality, joining multiple source tables, and applying business rules to determine valid referrals and reward eligibility.

---

## Data Profiling

Before any data cleaning or joins, basic data profiling is performed on all raw source tables to understand overall data quality and structure.

The profiling step includes:
- row counts per table
- null value counts for each column
- distinct value counts for each column

From the profiling results, most tables contain no missing values.  
The remaining null values mainly appear in reward- and transaction-related fields (e.g. reward ID, transaction ID), which is expected given the referral flow — not every referral leads to a completed transaction or reward.

This step helps confirm that missing values are meaningful and aligned with business logic rather than data quality issues.

The profiling output is saved as:

output/profiling_summary.csv


---

## Data Preprocessing

After profiling, the raw tables are joined using `user_referrals` as the base table to create a unified dataset for downstream analysis.

During preprocessing:
- referral status descriptions are mapped from status IDs
- transaction and reward information is joined where available
- referrer and referee user information is enriched from user logs
- timestamps are parsed and standardized
- referral timestamps are converted from UTC to the referrer’s local timezone
- a high-level referral source category is derived based on business rules:
  - **User Sign Up** → Online  
  - **Draft Transaction** → Offline  
  - **Lead** → original lead source category

The output of this step is a single cleaned dataset saved as:

output/preprocessed_referrals.csv


---

## Business Logic Validation

In the final step, business rules are applied to determine:
- whether a referral is valid
- whether a referral is eligible for a reward

The current rules include:
- a referral must have an associated transaction
- the transaction must be marked as paid
- the referrer account must not be deleted
- the transaction must occur after the referral timestamp
- reward eligibility depends on both referral validity and reward availability

The final validated dataset is saved as:

output/final_referral_results.csv


---

## Data Dictionary

To support non-technical stakeholders, a data dictionary is provided that explains each column in the final dataset, including its business meaning and source table.

The data dictionary is available as:

data_dictionary.xlsx


---

## Project Structure

springer-capital-referral-data-pipeline/
├── data/ # raw input CSV files
├── output/ # profiling, preprocessing, and final outputs
├── src/
│ ├── profiling.py # data profiling script
│ ├── preprocess.py # preprocessing and table joins
│ └── business_logic.py # business rule validation
├── Dockerfile
├── README.md
└── data_dictionary.xlsx


---

## Reproducibility

The full pipeline can be executed locally or inside a Docker container using the provided Dockerfile, ensuring consistent and reproducible results across environments.

---

## Notes

This project is designed as a simple end-to-end data pipeline to demonstrate data profiling, table joins, timezone handling, and rule-based validation in a real referral business context.
