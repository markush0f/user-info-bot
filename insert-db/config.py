import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    # Connection to db
    return psycopg2.connect(
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        dbname=os.getenv("DATABASE"),
        user=os.getenv("USER_DB"),
        password=os.getenv("PASSWORD_DB"),
        sslmode=os.getenv("SSL"),
    )
