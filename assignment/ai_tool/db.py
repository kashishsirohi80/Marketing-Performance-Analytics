from sqlalchemy import create_engine, text
import pandas as pd
from config import DB_URI

engine = create_engine(DB_URI)

def run_query(query: str):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        return str(e)