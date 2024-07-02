import sqlite3
import pandas as pd

# Function to retrieve events from the database
def get_events():
    conn = sqlite3.connect('economic_events.db')
    df = pd.read_sql_query('SELECT * FROM events', conn)
    conn.close()
    return df
