import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Access the password using os.getenv()
password = os.getenv("DB_password")

username = os.getenv("DB_username")

host = os.getenv("DB_host")
port = os.getenv("DB_port")
database = os.getenv("DB_database")

engine = create_engine(
    f"postgresql://{username}:{password}@{host}:{port}/{database}"
)

connection = engine.connect()

print("Connected successfully!")