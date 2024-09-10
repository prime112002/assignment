import pandas as pd
import numpy as np
import mysql.connector

def connect_to_database():
    print("Connecting to MySQL...")
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='stock_data_db'
    )
    print("Connected to MySQL database")
    return conn

def sma_strategy(df):
    # Calculate short and long moving averages
    short_window = 40
    long_window = 100

    df['short_sma'] = df['close'].rolling(window=short_window, min_periods=1).mean()
    df['long_sma'] = df['close'].rolling(window=long_window, min_periods=1).mean()

    # Generate signals
    df.loc[short_window:, 'signal'] = np.where(df['short_sma'][short_window:] > df['long_sma'][short_window:], 1, 0)
    df['signal'] = df['signal'].fillna(0)
    df['position'] = df['signal'].diff()
    
    return df

def fetch_data():
    conn = connect_to_database()
    query = "SELECT * FROM stock_data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    df = fetch_data()
    df = sma_strategy(df)
    print(df.head())
