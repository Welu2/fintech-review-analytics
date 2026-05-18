# Fintech Review Analytics Pipeline

An end-to-end data engineering pipeline designed to scrape, clean, process, and permanently store production customer sentiment records for Ethiopian banking applications in a secure relational PostgreSQL environment.

---

## 📈 Pipeline Performance Metrics
* **Total Clean Records Extracted**: 8,807 database lines (Exceeds the 1,200 assignment target KPI).
* **Missing Value Threshold**: <0.06% of the raw data (Exceeds the <5% maximum loss target KPI).
* **Deduplication Volume**: Removed 2,699 duplicate entries.

---

## 🛠️ Step 1: Data Collection & Preprocessing Architecture

### 1. Scraping Methodology
* **Tooling**: Python 3.10 runtime environment coupled with the operational `google-play-scraper` package.
* **Target Platforms**: Google Play Store.
* **Target App Configurations**:
  * **Commercial Bank of Ethiopia (CBE Bank)**: `com.combanketh.mobilebanking`
  * **Bank of Abyssinia**: `com.boa.boaMobileBanking`
  * **Dashen Bank**: `com.dashen.dashensuperapp`
* **Extraction Rules**: Set sorting flags to `Sort.NEWEST` to ensure comprehensive historical capture across all active application cycles.

### 2. Dataset Metrics Breakdown


| Financial Institution Asset | Total Sanitized Rows | Local Export Schema Structure |
| :--- | :--- | :--- |
| **Commercial Bank of Ethiopia** | 6,720 rows | `review`, `rating`, `date`, `bank`, `source` |
| **Bank of Abyssinia** | 1,219 rows | `review`, `rating`, `date`, `bank`, `source` |
| **Dashen Bank** | 868 rows | `review`, `rating`, `date`, `bank`, `source` |

### 3. Pipeline Hygiene Steps
* **Missing Value Management**: Dropped exactly 7 rows completely missing critical `review` or `rating` structures.
* **Deduplication Logic**: Consolidated data by isolating multi-column matches on `review`, `rating`, and `bank`.
* **Date Normalization**: Transformed inconsistent structural date strings into standard ISO `YYYY-MM-DD` timestamps.

---

## 🗄️ Step 2: Database Storage & Validation Setup

### 1. Database Schema Blueprints
The structure separates entity metadata from granular transactional reviews via normalized relational logic:

* **`banks` (Metadata Master)**: Holds system-generated primary keys, unique institution constraints, and public-facing workspace application identifiers.
* **`reviews` (Transactional Ledger)**: Houses text arrays, integer boundaries for star scales, analytical output parameters (sentiment properties), tracking flags, and a cascade foreign key constraint targeting entity drops safely.

### 2. Environment Prerequisites
1. Ensure a PostgreSQL server instance is live on your target system.
2. Spin up a designated database target instance named exactly: `bank_reviews`.
3. Fill out and save a local environment file named `.env` in your root environment workspace using the following configuration layout:

```env
DB_username=your_postgres_user
DB_password=your_secure_password
DB_host=localhost
DB_port=5432
DB_database=bank_reviews
```

### 3. Execution Protocols
Install the required application dependencies and trigger the automatic ingestion mapping runtime engine using terminal execution parameters:
```bash
pip install -r requirements.txt
python src/insert_data.py
```

### 4. Continuous Data Integrity Validation Audit Log
The framework automatically checks relational integrity parameters on live data. The output logs captured during runtime confirm valid counts, zero data loss, and perfect schema compliance:

```text
Connected to PostgreSQL successfully!
Database tables validated/created successfully.
Syncing 3 banks with database...
Inserting 8807 processing reviews into database...
Reviews batch insertion completed successfully!

==============================================
      RUNNING INTEGRITY VERIFICATION QUERIES   
==============================================

[Metric Check] Review Count & Average Rating per Bank:
 - CBE Bank: Total Reviews = 6720 | Avg Rating = 3.82
 - Dashen Bank: Total Reviews = 868  | Avg Rating = 4.04
 - Bank of Abyssinia: Total Reviews = 1219 | Avg Rating = 2.96

[Hygiene Check] Missing Value Analysis in Crucial Columns:
 - Null Bank Foreign Keys: 0
 - Null Review Texts: 0
 - Null Review Ratings: 0

All pipeline tasks executed perfectly!
```

---

## ⚠️ Pipeline Constraints & Operational Frontiers
* **Language Profiling Restrictions**: The filtering engine blocks non-English datasets. Any user reviews published natively utilizing Ge'ez syntax, Amharic configurations, or alternative regional variations are omitted from analysis.
* **Text Variable Volume Ranges**: Text entry lengths fluctuate between single-character keywords and long paragraphs, requiring downstream text sequence management protocols for deep NLP modeling tasks.
