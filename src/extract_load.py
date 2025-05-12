import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

commodities = ['CL=F', 'GC=F', 'SI=F']

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

def search_commodities_data(symbol, period='5y', interval='1d'):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period = period, interval = interval)
    data['symbol'] = symbol
    return data

def search_all_commodities_data(commodities):
    all_data = []
    for symbol in commodities:
        data = search_commodities_data(symbol)
        all_data.append(data)
    return pd.concat(all_data)

def save_on_postgres(df, schema = 'public'):
    df.to_sql('commodities', engine, if_exists = 'replace', index=True, index_label='Date', schema=schema)

if __name__ == "__main__":
    concat_data = search_all_commodities_data(commodities)
    save_on_postgres(concat_data, schema = 'public')