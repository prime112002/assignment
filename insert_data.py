import pandas as pd
import mysql.connector
from mysql.connector import Error

try:
    # Connect to MySQL database
    print("Connecting to MySQL...")
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="",  
        database="stock_data_db"  
    )

    if conn.is_connected():
        print("Connected to MySQL database")

    cursor = conn.cursor()

    # Load CSV data into pandas DataFrame
    csv_file = '/home/satwik/invsto assignment/HINDALCO_1D.xlsx - HINDALCO.csv'  
    df = pd.read_csv(csv_file)
    
    # Print column names to verify
    print("Column names in CSV file:", df.columns.tolist())

    # Insert data row by row into MySQL table
    for index, row in df.iterrows():
        sql = """
            INSERT INTO stock_data (instrument, datetime, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            row['instrument'],  
            row['datetime'],   
            row['open'],        
            row['high'],        
            row['low'],         
            row['close'],       
            row['volume']       
        )
        cursor.execute(sql, data)

    # Commit the transaction
    conn.commit()
    print("Data inserted successfully")

except Error as e:
    print(f"Error: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")
