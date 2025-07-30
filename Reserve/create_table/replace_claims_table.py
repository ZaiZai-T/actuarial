# 文件：replace_claims_table.py
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus

def replace_claims_table():
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE_PATH = os.path.join(CURRENT_DIR, "../data/simulated_claims_data_strict_sorted.csv")

    load_dotenv()
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)

    engine_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(engine_url)

    df = pd.read_csv(DATA_FILE_PATH)
    df.to_sql("insurance_claims", engine, index=False, if_exists="replace")

    print("Succeed New Table! ")
