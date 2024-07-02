import sqlite3
import pytest
from data_fetcher import fetch_economic_events
from data_storer import create_table, store_events, get_events
from email_sender import send_email

# Define the name of the test database
TEST_DB = 'test_economic_events.db'

def setup_module(module):
    """
    Setup function to create the table in the test database before any tests are run.

    Args:
        module: The module that contains the tests.
    """
    create_table(TEST_DB)

def teardown_function(function):
    """
    Teardown function to clean up the test database after each test function.

    Args:
        function: The test function that was just run.
    """
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    c.execute('DELETE FROM events')
    conn.commit()
    conn.close()

def test_integration_fetch_store_get():
    """
    Integration test to fetch economic events, store them in the database, and retrieve them.

    Asserts:
        - The fetched events are a non-empty list.
        - The retrieved events from the database are a non-empty DataFrame.
    """
    # Fetch economic events
    events = fetch_economic_events()
    assert isinstance(events, list)
    assert len(events) > 0

    # Store the events in the test database
    store_events(events, TEST_DB)

    # Retrieve the events from the test database
    retrieved_events = get_events(TEST_DB)
    assert not retrieved_events.empty
    assert len(retrieved_events) > 0

def test_integration_fetch_store_send_email(mocker):
    """
    Integration test to fetch economic events, store them in the database, retrieve them, and send an email.

    Args:
        mocker: The mocker fixture for mocking external dependencies.

    Asserts:
        - The fetched events are a non-empty list.
        - The retrieved events from the database are a non-empty DataFrame.
        - The email is sent successfully.
        - The Dispatch method is called exactly once.
    """
    # Fetch economic events
    events = fetch_economic_events()
    assert isinstance(events, list)
    assert len(events) > 0

    # Store the events in the test database
    store_events(events, TEST_DB)

    # Retrieve the events from the test database
    retrieved_events = get_events(TEST_DB)
    assert not retrieved_events.empty
    assert len(retrieved_events) > 0

    # Mock the Dispatch method from the win32com.client module
    mock_dispatch = mocker.patch('win32com.client.Dispatch')

    # Send an email with the retrieved events
    status = send_email(retrieved_events.to_dict('records'), "test@example.com", "Test Email", "This is a test email.")
    assert status == "Email sent!"
    mock_dispatch.assert_called_once()
