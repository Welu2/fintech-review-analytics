# Fintech Review Analytics

## Task 1: Data Collection & Preprocessing

### 1. Scraping Methodology
* **Tooling**: Built using Python 3.10 and the `google-play-scraper` library.
* **Target Source**: Google Play Store (`source: Google Play`).
* **Target Applications**: 
  * Commercial Bank of Ethiopia (CBE Bank) - `com.combanketh.mobilebanking`
  * Bank of Abyssinia - `com.boa.boaMobileBanking`
  * Dashen Bank - `com.dashen.dashensuperapp`
* **Execution Strategy**: Extracted all available English-language reviews using `Sort.NEWEST` to ensure comprehensive historical capture.

### 2. Dataset Metrics & Date Ranges
* **CBE Bank**: 6,719 clean reviews (Range: [INSERT MIN DATE] to [INSERT MAX DATE])
* **Bank of Abyssinia**: 1,219 clean reviews (Range: [INSERT MIN DATE] to [INSERT MAX DATE])
* **Dashen Bank**: 868 clean reviews (Range: [INSERT MIN DATE] to [INSERT MAX DATE])
* **Total Clean Records**: 8,806 lines (Exceeds the 1,200 assignment target KPI).

### 3. Preprocessing Pipeline & Data Hygiene
* **Missing Values**: Dropped exactly 7 records missing critical content (`review` text or `rating`). Missing data accounts for <0.06% of the raw pull, easily passing the <5% target KPI.
* **Deduplication**: Eliminated 2,699 redundant rows using multi-column matching (`review`, `rating`, `bank`).
* **Date Normalization**: Standardized all regional timestamp structures into ISO `YYYY-MM-DD` string objects.
* **Schema Integrity**: The final local export isolates exactly five specified columns: `review`, `rating`, `date`, `bank`, `source`.

### 4. Encountered Limitations
* **Language Constraints**: The filter limits extraction to English (`lang='en'`). Relevant feedback posted exclusively in Amharic (using Latin or Ge'ez scripts) or other regional languages was not parsed.
* **Character Fields**: Review lengths vary significantly from single-word entries to detailed reports, requiring text sequence handling in future analytical tasks.
