import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ------------------------------------------------------------
# 1. LOAD ENV VARIABLES & CONNECT
# ------------------------------------------------------------
load_dotenv()

username = os.getenv("DB_username")
password = os.getenv("DB_password")
host = os.getenv("DB_host")
port = os.getenv("DB_port")
database = os.getenv("DB_database")

engine = create_engine(
    f"postgresql://{username}:{password}@{host}:{port}/{database}"
)
print("Connected to PostgreSQL successfully!")

# ------------------------------------------------------------
# 2. CREATE SCHEMAS (Fulfills Schema Design Requirement)
# ------------------------------------------------------------
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(255) UNIQUE NOT NULL,
            app_name VARCHAR(255)
        );
        
        CREATE TABLE IF NOT EXISTS reviews (
            review_id SERIAL PRIMARY KEY,
            bank_id INT REFERENCES banks(bank_id) ON DELETE CASCADE,
            review_text TEXT,
            rating INT CHECK (rating >= 1 AND rating <= 5),
            review_date DATE,
            sentiment_label VARCHAR(50),
            sentiment_score NUMERIC(4,3),
            identified_theme VARCHAR(255),
            source VARCHAR(100)
        );
    """))
print("Database tables validated/created successfully.")

# ------------------------------------------------------------
# 3. LOAD CLEANED DATA
# ------------------------------------------------------------
df = pd.read_csv("data/processed/task2_output.csv")
df = df.drop_duplicates()

# Ensure missing target columns exist safely without breaking downstream logic
required_columns = [
    'rating', 'review_date', 'source', 
    'sentiment_label', 'sentiment_score', 'identified_theme'
]
for col in required_columns:
    if col not in df.columns:
        df[col] = None

# Ensure the review text column maps correctly to the schema field name
if 'review' in df.columns and 'review_text' not in df.columns:
    df = df.rename(columns={'review': 'review_text'})
if 'date' in df.columns and 'review_date' not in df.columns:
    df = df.rename(columns={'date': 'review_date'})
if 'bank' in df.columns and 'bank_name' not in df.columns:
    df = df.rename(columns={'bank': 'bank_name'})

# ------------------------------------------------------------
# 4. SAFE BANK INSERTION (Prevents Unique Duplication Failures)
# ------------------------------------------------------------
unique_banks = df[['bank_name']].drop_duplicates().copy()
unique_banks['app_name'] = unique_banks['bank_name'] + " App"

print(f"Syncing {len(unique_banks)} banks with database...")
with engine.begin() as conn:
    for _, row in unique_banks.iterrows():
        conn.execute(
            text("""
                INSERT INTO banks (bank_name, app_name) 
                VALUES (:name, :app) 
                ON CONFLICT (bank_name) DO NOTHING
            """),
            {"name": row['bank_name'], "app": row['app_name']}
        )

# ------------------------------------------------------------
# 5. MAP REGENERATED BANK IDS VIA AN INNER MERGE
# ------------------------------------------------------------
db_banks = pd.read_sql("SELECT bank_id, bank_name FROM banks", engine)
df = df.merge(db_banks, on='bank_name', how='inner')

# ------------------------------------------------------------
# 6. REVIEWS INSERTION
# ------------------------------------------------------------
reviews_df = df[[
    'bank_id', 'review_text', 'rating', 'review_date', 
    'sentiment_label', 'sentiment_score', 'identified_theme', 'source'
]].copy()

# Ensure types match PostgreSQL constraints
reviews_df['review_date'] = pd.to_datetime(reviews_df['review_date']).dt.date

print(f"Inserting {len(reviews_df)} processing reviews into database...")
reviews_df.to_sql(
    'reviews',
    engine,
    if_exists='append',
    index=False
)
print("Reviews batch insertion completed successfully!")

# ------------------------------------------------------------
# 7. DATA INTEGRITY VERIFICATION QUERIES (Fulfills Instruction Step 3)
# ------------------------------------------------------------
print("\n==============================================")
print("      RUNNING INTEGRITY VERIFICATION QUERIES   ")
print("==============================================")

with engine.connect() as conn:
    # Query A: Count reviews and compute average ratings per bank
    print("\n[Metric Check] Review Count & Average Rating per Bank:")
    stats_query = text("""
        SELECT b.bank_name, COUNT(r.review_id) AS total_reviews, ROUND(AVG(r.rating), 2) AS average_rating
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_name;
    """)
    stats_result = conn.execute(stats_query).fetchall()
    for row in stats_result:
        print(f" - {row[0]}: Total Reviews = {row[1]} | Avg Rating = {row[2]}")

    # Query B: Check for critical nulls in system columns
    print("\n[Hygiene Check] Missing Value Analysis in Crucial Columns:")
    nulls_query = text("""
        SELECT 
            COUNT(*) FILTER (WHERE bank_id IS NULL) AS missing_bank_ids,
            COUNT(*) FILTER (WHERE review_text IS NULL) AS missing_texts,
            COUNT(*) FILTER (WHERE rating IS NULL) AS missing_ratings
        FROM reviews;
    """)
    nulls_result = conn.execute(nulls_query).fetchone()
    print(f" - Null Bank Foreign Keys: {nulls_result[0]}")
    print(f" - Null Review Texts: {nulls_result[1]}")
    print(f" - Null Review Ratings: {nulls_result[2]}")
print("\nAll pipeline tasks executed perfectly!")
