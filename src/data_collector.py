import os
import pandas as pd
from google_play_scraper import Sort, reviews_all

def collect_and_clean_reviews():
    # 1. Target Apps mapped to their official Play Store package IDs
    target_apps = {
        "CBE Bank": "com.combanketh.mobilebanking",       # Commercial Bank of Ethiopia
        "Bank of Abyssinia": "com.boa.boaMobileBanking",  # BoA Mobile
        "Dashen Bank": "com.dashen.dashensuperapp"        # Dashen SuperApp
    }
    
    combined_reviews = []
    
    # 2. Scraping Phase
    for bank_name, app_id in target_apps.items():
        print(f"--- Starting scrape for {bank_name} ({app_id}) ---")
        try:
            # reviews_all downloads records sequentially in background chunks
            raw_data = reviews_all(
                app_id,
                lang='en', 
                country='us', 
                sort=Sort.NEWEST
            )
            print(f"Successfully pulled {len(raw_data)} raw reviews from {bank_name}.")
            
            # Map API fields directly to assignment specs
            for item in raw_data:
                combined_reviews.append({
                    'review': item.get('content'),
                    'rating': item.get('score'),
                    'date': item.get('at'),
                    'bank': bank_name,
                    'source': 'Google Play'
                })
                
        except Exception as error:
            print(f"CRITICAL ERROR scraping {bank_name}: {error}")
            print("Skipping to next bank...")

    # Verify we actually got data before doing math operations
    if not combined_reviews:
        print("Error: No data was collected from any app. Check your internet connection.")
        return

    # Convert array into a structural Pandas DataFrame for easy tracking
    df = pd.DataFrame(combined_reviews)
    print(f"\n--- Scraping complete. Total records gathered: {len(df)} ---")

    # 3. Step-by-Step Preprocessing Pipeline (Easy to isolate and debug)
    print("\n[Pipeline Step 1] Cleaning Missing Values...")
    initial_rows = len(df)
    df = df.dropna(subset=['review', 'rating'])
    print(f"Dropped {initial_rows - len(df)} empty rows.")

    print("\n[Pipeline Step 2] Removing Exact Duplicates...")
    before_dedup = len(df)
    df = df.drop_duplicates(subset=['review', 'rating', 'bank'])
    print(f"Dropped {before_dedup - len(df)} duplicate reviews.")

    print("\n[Pipeline Step 3] Normalizing Date Structures...")
    # Convert dates safely to standard string format YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    print("Dates successfully transformed.")

    # 4. Storage Phase
    print("\n[Pipeline Step 4] Writing Dataset to Local Disk...")
    os.makedirs('data/raw', exist_ok=True)
    output_file = 'data/raw/cleaned_reviews.csv'
    
    df.to_csv(output_file, index=False)
    print(f"SUCCESS: Safe, untracked dataset built at '{output_file}' with {len(df)} lines.")
    
    # Debug Summary Matrix to console
    print("\nFinal clean count breakdown per bank:")
    print(df['bank'].value_counts())

if __name__ == "__main__":
    collect_and_clean_reviews()
