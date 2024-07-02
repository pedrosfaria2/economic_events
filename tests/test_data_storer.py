import pytest
import sqlite3
from data_storer import create_table, store_events, get_events

# Define the name of the test database
TEST_DB = 'test_economic_events.db'

def setup_module(module):
    """
    Setup function to create the database table before running any tests.
    This function is called once per module.
    """
    create_table(TEST_DB)

def teardown_function(function):
    """
    Teardown function to clean up the database after each test function.
    This ensures that each test starts with a clean state.
    """
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    c.execute('DELETE FROM events')
    conn.commit()
    conn.close()

def test_store_and_get_events():
    """
    Test the store_events and get_events functions to ensure they correctly
    store and retrieve events from the database.

    This test performs the following checks:
    1. Store a list of test events in the database.
    2. Retrieve the events from the database.
    3. Ensure the retrieved DataFrame is not empty.
    4. Ensure there is at least one event in the DataFrame.
    5. Check if the stored event matches the test event.
    """
    # Define a list of test events
    test_events = [
        {
            'Date': '12/25/23',
            'Time': '08:30',
            'Currency': 'USD',
            'Volatility': 'High',
            'Event': 'Test Event',
            'Forecast': '123',
            'Previous': '100'
        }
    ]
    # Store the test events in the database
    store_events(test_events, TEST_DB)
    # Retrieve the events from the database
    events = get_events(TEST_DB)
    
    # Ensure the retrieved DataFrame is not empty
    assert not events.empty
    # Ensure there is at least one event in the DataFrame
    assert len(events) > 0
    
    # Check if the stored event matches the test event
    event = events[(events['Date'] == '12/25/23') & 
                   (events['Time'] == '08:30') & 
                   (events['Currency'] == 'USD') & 
                   (events['Event'] == 'Test Event')]
    assert not event.empty
    assert event.iloc[0]['Date'] == '12/25/23'
    assert event.iloc[0]['Time'] == '08:30'
    assert event.iloc[0]['Currency'] == 'USD'
    assert event.iloc[0]['Volatility'] == 'High'
    assert event.iloc[0]['Event'] == 'Test Event'
    assert event.iloc[0]['Forecast'] == '123'
    assert event.iloc[0]['Previous'] == '100'

def test_store_events_database_error(mocker):
    """
    Test the store_events function to handle database errors gracefully.

    This test performs the following checks:
    1. Mock the sqlite3.connect method to raise an Exception simulating a database error.
    2. Ensure the store_events function raises an Exception with the expected message.
    """
    # Mock the sqlite3.connect method to raise an Exception with the message "Database Error"
    mocker.patch('sqlite3.connect', side_effect=Exception("Database Error"))

    # Define a list of test events
    test_events = [
        {
            'Date': '12/25/23',
            'Time': '08:30',
            'Currency': 'USD',
            'Volatility': 'High',
            'Event': 'Test Event',
            'Forecast': '123',
            'Previous': '100'
        }
    ]
    
    # Ensure the store_events function raises an Exception with the expected message
    with pytest.raises(Exception, match="Database Error"):
        store_events(test_events, TEST_DB)

def test_get_events_database_error(mocker):
    """
    Test the get_events function to handle database errors gracefully.

    This test performs the following checks:
    1. Mock the sqlite3.connect method to raise an Exception simulating a database error.
    2. Ensure the get_events function raises an Exception with the expected message.
    """
    # Mock the sqlite3.connect method to raise an Exception with the message "Database Error"
    mocker.patch('sqlite3.connect', side_effect=Exception("Database Error"))

    # Ensure the get_events function raises an Exception with the expected message
    with pytest.raises(Exception, match="Database Error"):
        get_events(TEST_DB)
