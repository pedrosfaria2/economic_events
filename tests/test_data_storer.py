import pytest
import sqlite3
from data_storer import create_table, store_events, get_events

TEST_DB = 'test_economic_events.db'

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    create_table(TEST_DB)

def teardown_function(function):
    """ clean up after each test function """
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    c.execute('DELETE FROM events')
    conn.commit()
    conn.close()

def test_store_and_get_events():
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
    store_events(test_events, TEST_DB)
    events = get_events(TEST_DB)
    assert not events.empty
    assert len(events) > 0
    
    # Verifica se o evento armazenado corresponde ao evento de teste
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
