import sqlite3
import pandas as pd

# Function to create the events table if it does not exist
def create_table(db_name='economic_events.db'):
    """
    Create the events table if it does not exist.

    Parameters:
    db_name (str): The name of the database file. Default is 'economic_events.db'.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (Date TEXT, Time TEXT, Currency TEXT, Volatility TEXT, Event TEXT, Forecast TEXT, Previous TEXT)''')
    conn.commit()
    conn.close()

# Function to store events in the database
def store_events(events, db_name='economic_events.db'):
    """
    Store events in the database.

    Parameters:
    events (list of dict): A list of events, where each event is a dictionary containing event details.
    db_name (str): The name of the database file. Default is 'economic_events.db'.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    # Add only new events
    for event in events:
        c.execute('''SELECT * FROM events WHERE Date=? AND Time=? AND Currency=? AND Event=?''',
                  (event['Date'], event['Time'], event['Currency'], event['Event']))
        if not c.fetchone():
            c.execute('INSERT INTO events (Date, Time, Currency, Volatility, Event, Forecast, Previous) VALUES (?, ?, ?, ?, ?, ?, ?)',
                      (event['Date'], event['Time'], event['Currency'], event['Volatility'], event['Event'], event['Forecast'], event['Previous']))
    
    conn.commit()
    conn.close()

# Function to retrieve events from the database
def get_events(db_name='economic_events.db'):
    """
    Retrieve events from the database.

    Parameters:
    db_name (str): The name of the database file. Default is 'economic_events.db'.

    Returns:
    pandas.DataFrame: A DataFrame containing all events from the database.
    """
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query('SELECT * FROM events', conn)
    conn.close()
    return df

# Initialize the database and create the table if it does not exist
create_table()
