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

## 📊 Step 4: Insights, Visualizations & Recommendations

### 1. Analytical Visualizations Dashboard
The automated pipeline executes token text cleaning alongside statutory statistical distributions. It generates, saves, and updates 5 structural assets inside the `/reports/figures/` directory:

* `sentiment_distribution.png`: Stacked bar chart profiling positive vs. negative volume balances across institutions.
* `rating_distribution.png`: Boxplot isolating rating medians, IQR spread, and density distributions per platform.
* `[bank_name]_keywords.png`: Horizontal bar chart plotting the top 10 unique, non-stopword tokens.
* `[bank_name]_wordcloud.png`: High-density visual word layouts showing qualitative customer feedback weightings.
* `sentiment_trend.png`: A comprehensive monthly rolling line chart tracking structural historical sentiment changes.

### 2. Cross-Bank Comparative Assessment Matrix


| Dimension | Commercial Bank of Ethiopia (CBE) | Bank of Abyssinia (BoA) | Dashen Bank |
| :--- | :--- | :--- | :--- |
| **Overall Sentiment** | High volume, split between strong loyalty and severe transaction friction. | Highly polarized; suffering from explicit software development team criticism. | Balanced; lower review volume with stable utility scores. |
| **Average Rating** | Moderate (Driven by sheer user base scale). | Low (Pulled down heavily by recent stability updates). | Moderate-High (Stable user experience). |
| **Dominant Theme** | Core Transaction Engine Reliability. | Application Architecture & Latency. | Interface Usability & Feature Navigation. |

### 3. Deep-Dive Grounded Insights & Action Plans

#### 🏦 Commercial Bank of Ethiopia (CBE)
* **Top 2 Satisfaction Drivers**:
  * **Easy** (Mentioned 332 times): Users find the UI accessible and intuitive during stable runtime environments.
  * **Fast** (Mentioned 192 times): Core query workflows and regional processing operations score efficiently.
* **Top 2 Critical Pain Points**:
  * **Transaction** (Mentioned 212 times): Timeout issues and network execution blocks on processing pathways.
  * **Money** (Mentioned 188 times): Disconnects between localized ledger states and live customer balances.
* **Engineering Actions**:
  1. Refactor distributed background database transaction pipelines to systematically clear transactional deadlocks.
  2. Deploy secure client-side idempotent transaction IDs to handle mid-request network drops without double-debiting.

#### 🏦 Bank of Abyssinia (BoA)
* **Top 2 Satisfaction Drivers**:
  * **Fast** (Mentioned 20 times): Initial layout painting velocities and micro-animations score favorably.
  * **Service** (Mentioned 19 times): Digital self-service options decrease customer reliance on brick-and-mortar branches.
* **Top 2 Critical Pain Points**:
  * **Developer** (Mentioned 45 times): Customers explicitly target build stability degradation and patch regressions.
  * **Slow / Version** (Combined 34+ times): Massive degradation of processing velocity directly related to explicit system versions.
* **Engineering Actions**:
  1. Dedicate a focused hotfix sprint pipeline targeting main-thread memory leaks and multi-core thread blocking.
  2. Implement a pre-release matrix pipeline executing automated integration and layout compatibility checks across diverse legacy OS variants.

#### 🏦 Dashen Bank
* **Top 2 Satisfaction Drivers**:
  * **Easy** (Mentioned 65 times): User layout structures support flat, shallow navigation pathways.
  * **Fast** (Mentioned 64 times): Peer-to-peer asset movements and internal queries post low processing durations.
* **Top 2 Critical Pain Points**:
  * **Slow** (Mentioned 25 times): Microservice API orchestration overhead stalls integration processing flows.
  * **Account** (Mentioned 22 times): Unexpected runtime auth-token exceptions forcefully logging out active sessions.
* **Engineering Actions**:
  1. Minimize redundant state re-rendering sequences and implement local key-value data caching strategies.
  2. Review security token lifecycle configurations to extend secure active-session lifetimes while users construct payloads.

---

## ⚠️ Pipeline Constraints & Operational Frontiers
* **Language Profiling Restrictions**: The filtering engine blocks non-English datasets. Any user reviews published natively utilizing Ge'ez syntax, Amharic configurations, or alternative regional variations are omitted from analysis.
* **Text Variable Volume Ranges**: Text entry lengths fluctuate between single-character keywords and long paragraphs, requiring downstream text sequence management protocols for deep NLP modeling tasks.
* **Negativity Bias**: App reviews are highly vulnerable to voluntary response bias. Disgruntled customers experiencing failures are disproportionately represented compared to passive, satisfied cohorts.
* **Sampling Bias**: Scraped metrics capture distinct software production releases. They are inherently prone to short-term data spikes during major system blackouts or unoptimized feature rollouts.
