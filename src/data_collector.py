# ============================================================
# TASK 1: DATA COLLECTION + PREPROCESSING
# ============================================================

import os
import pandas as pd

from google_play_scraper import (
    Sort,
    reviews_all
)


# ============================================================
# MAIN SCRAPING PIPELINE
# ============================================================

def collect_and_clean_reviews():

    # --------------------------------------------------------
    # TARGET APPLICATIONS
    # --------------------------------------------------------

    target_apps = {

        "CBE Bank":
            "com.combanketh.mobilebanking",

        "Bank of Abyssinia":
            "com.boa.boaMobileBanking",

        "Dashen Bank":
            "com.dashen.dashensuperapp"
    }

    combined_reviews = []

    # --------------------------------------------------------
    # SCRAPING PHASE
    # --------------------------------------------------------

    for bank_name, app_id in target_apps.items():

        print(f"\n--- Scraping {bank_name} ---")

        try:

            raw_data = reviews_all(
                app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST
            )

            print(
                f"Collected {len(raw_data)} raw reviews "
                f"from {bank_name}."
            )

            # KPI validation
            if len(raw_data) < 400:

                print(
                    f"WARNING: Only {len(raw_data)} reviews "
                    f"collected for {bank_name}."
                )

            # Map fields
            for item in raw_data:

                combined_reviews.append({

                    'review':
                        item.get('content'),

                    'rating':
                        item.get('score'),

                    'date':
                        item.get('at'),

                    'bank':
                        bank_name,

                    'source':
                        'Google Play'
                })

        except Exception as error:

            print(
                f"ERROR scraping {bank_name}: {error}"
            )

            print("Skipping to next app...")

    # --------------------------------------------------------
    # VALIDATE COLLECTION
    # --------------------------------------------------------

    if not combined_reviews:

        print(
            "ERROR: No reviews collected."
        )

        return

    # --------------------------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------------------------

    df = pd.DataFrame(combined_reviews)

    print(
        f"\nTotal Raw Reviews Collected: {len(df)}"
    )

    # --------------------------------------------------------
    # MISSING VALUE ANALYSIS
    # --------------------------------------------------------

    print("\n=== Missing Value Analysis ===")

    missing_reviews = df['review'].isnull().sum()
    missing_ratings = df['rating'].isnull().sum()

    print(f"Missing Reviews: {missing_reviews}")
    print(f"Missing Ratings: {missing_ratings}")

    missing_percentage = (

        (missing_reviews + missing_ratings)

        / (len(df) * 2)

    ) * 100

    print(
        f"Missing Data Percentage: "
        f"{missing_percentage:.2f}%"
    )

    # --------------------------------------------------------
    # REMOVE MISSING VALUES
    # --------------------------------------------------------

    print("\nRemoving missing rows...")

    initial_rows = len(df)

    df = df.dropna(
        subset=['review', 'rating']
    )

    print(
        f"Removed {initial_rows - len(df)} rows."
    )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    print("\nRemoving duplicate reviews...")

    before_dedup = len(df)

    df = df.drop_duplicates(
        subset=['review', 'rating', 'bank']
    )

    print(
        f"Removed {before_dedup - len(df)} duplicates."
    )

    # --------------------------------------------------------
    # DATE NORMALIZATION
    # --------------------------------------------------------

    print("\nNormalizing date formats...")

    df['date'] = (
        pd.to_datetime(df['date'])
        .dt.strftime('%Y-%m-%d')
    )

    print("Date normalization complete.")

    # --------------------------------------------------------
    # FINAL SCHEMA VALIDATION
    # --------------------------------------------------------

    required_columns = [

        'review',
        'rating',
        'date',
        'bank',
        'source'
    ]

    print("\nFinal Dataset Columns:")

    print(df.columns.tolist())

    assert all(
        col in df.columns
        for col in required_columns
    ), "Dataset schema mismatch!"

    # --------------------------------------------------------
    # SAVE CLEAN DATASET
    # --------------------------------------------------------

    print("\nSaving cleaned dataset...")

    os.makedirs(
        'data/raw',
        exist_ok=True
    )

    output_file = (
        'data/raw/cleaned_reviews.csv'
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nSUCCESS: Dataset saved to:\n"
        f"{output_file}"
    )

    print(
        f"\nFinal Dataset Size: {len(df)}"
    )

    # --------------------------------------------------------
    # FINAL KPI BREAKDOWN
    # --------------------------------------------------------

    print("\n=== Reviews Per Bank ===")

    print(df['bank'].value_counts())

    print("\n=== Sample Rows ===")

    print(df.head())


# ============================================================
# SCRIPT ENTRYPOINT
# ============================================================

if __name__ == "__main__":

    collect_and_clean_reviews()