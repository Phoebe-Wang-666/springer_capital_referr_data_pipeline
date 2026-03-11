# springer-capital-referral-data-pipeline

A Python-based data pipeline for profiling, preprocessing, and validating referral data, built as part of the Springer Capital internship program.

This project demonstrates a simple end-to-end data workflow that analyzes referral program data, joins multiple source tables, and applies business rules to determine valid referrals and reward eligibility.

---

# Pipeline Overview

The pipeline processes referral program data in three stages:

1. **Data Profiling**  
   Analyze raw datasets to understand data quality, including null values and distinct counts.

2. **Data Preprocessing**  
   Clean and join multiple source tables to create a unified dataset based on the `user_referrals` table.

3. **Business Logic Validation**  
   Apply business rules to determine valid referrals and reward eligibility.

### Workflow

```
Raw CSV Data
      ↓
Data Profiling
      ↓
Data Preprocessing & Table Joins
      ↓
Business Logic Validation
      ↓
Final Validated Referral Dataset
```

---

# Environment Requirements

This project requires:

- Python 3.9+
- pandas
- numpy

Install dependencies with:

```bash
pip install pandas numpy
```

---

# How to Run the Pipeline

1. Place all raw CSV files in the `data/` directory.

2. Run the **data profiling** step:

```bash
python src/profiling.py
```

This generates:

```
output/profiling_summary.csv
```

3. Run the **data preprocessing** step:

```bash
python src/preprocess.py
```

This generates:

```
output/preprocessed_referrals.csv
```

4. Run the **business logic validation** step:

```bash
python src/business_logic.py
```

This generates:

```
output/final_referral_results.csv
```

---

# Output Files

The pipeline produces three main outputs in the `output/` directory.

### profiling_summary.csv

Contains data profiling results for each table and column, including:

- null value counts
- distinct value counts

This step helps identify potential data quality issues before transformations.

---

### preprocessed_referrals.csv

A cleaned dataset created by joining multiple source tables using `user_referrals` as the base table.

Key transformations include:

- mapping referral status descriptions
- joining transaction and reward information
- enriching referrer and referee user information
- parsing timestamps
- converting referral timestamps from UTC to the referrer’s local timezone
- deriving referral source categories

---

### final_referral_results.csv

The final validated dataset after applying business rules.

Additional fields include:

- `is_valid_referral`
- `invalid_reason`
- `is_reward_eligible`

These fields indicate whether a referral satisfies the business rules and qualifies for a reward.

---

# Data Profiling

Before any data cleaning or joins, basic profiling is performed on all raw source tables to understand overall data quality and structure.

The profiling step calculates:

- row counts
- null value counts
- distinct value counts

Most tables contain no missing values. Remaining null values mainly appear in reward and transaction fields (e.g., reward ID or transaction ID), which is expected because not all referrals lead to completed transactions or rewards.

---

# Data Preprocessing

During preprocessing, multiple tables are joined and cleaned using `user_referrals` as the base table.

Key transformations include:

- mapping referral status descriptions from status IDs
- joining reward and transaction information
- enriching referrer and referee user data
- parsing timestamps
- converting timestamps from UTC to the referrer’s local timezone
- deriving high-level referral source categories

Example mappings:

- **User Sign Up → Online**
- **Draft Transaction → Offline**
- **Lead → original lead source category**

---

# Business Logic Validation

In the final stage, business rules are applied to determine whether a referral is valid and whether it qualifies for a reward.

Current rules include:

- a referral must have an associated transaction
- the transaction must be marked as **PAID**
- the referrer account must not be deleted
- the transaction must occur **after** the referral timestamp
- reward eligibility depends on both referral validity and reward availability

---

# Running with Docker

You can also run the pipeline inside a Docker container.

Build the container:

```bash
docker build -t referral-pipeline .
```

Run the container:

```bash
docker run referral-pipeline
```

---

# Data Dictionary

To support non-technical stakeholders, a data dictionary is included describing each column in the dataset and its business meaning.

File location:

```
data_dictionary.xlsx
```

---

# Project Structure

```
springer-capital-referral-data-pipeline/
├── data/                 # raw input CSV files
├── output/               # pipeline outputs
├── src/
│   ├── profiling.py      # data profiling script
│   ├── preprocess.py     # preprocessing and table joins
│   └── business_logic.py # business rule validation
├── Dockerfile
├── README.md
└── data_dictionary.xlsx
```

---

# Reproducibility

The entire pipeline can be executed locally or inside Docker using the provided scripts and container configuration, ensuring consistent and reproducible results across environments.

---

# Notes

This project demonstrates a simple end-to-end data pipeline that integrates data profiling, table joins, timezone handling, and rule-based validation in a referral program context.