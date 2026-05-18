import os
import pytest
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def test_database_connection():
    # Provide safe default fallbacks if environment variables are missing on GitHub
    username = os.getenv("DB_username", "postgres")
    password = os.getenv("DB_password", "postgres")
    host = os.getenv("DB_host", "localhost")
    database = os.getenv("DB_database", "bank_reviews")
    
    # Read port safely, default to 5432 if None or empty
    port_env = os.getenv("DB_port")
    port = int(port_env) if port_env and port_env != "None" else 5432

    # Skip actual connection verification if running in a GitHub environment without a live DB
    if os.getenv("GITHUB_ACTIONS") == "true":
        pytest.skip("Skipping live database connection test inside GitHub Actions container.")

    engine = create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{database}"
    )
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1;")).fetchone()
        assert result[0] == 1
