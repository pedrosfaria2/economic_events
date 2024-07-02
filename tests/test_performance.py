import time
import pytest
from data_fetcher import fetch_economic_events
from data_storer import store_events, get_events
import platform

if platform.system() == "Windows":
    from email_sender import send_email

# Define acceptable time limits in seconds
FETCH_EVENTS_TIME_LIMIT = 10  # Maximum acceptable time for fetching events
STORE_EVENTS_TIME_LIMIT = 2   # Maximum acceptable time for storing events
GET_EVENTS_TIME_LIMIT = 2     # Maximum acceptable time for retrieving events
SEND_EMAIL_TIME_LIMIT = 2     # Maximum acceptable time for sending an email

# Test function for performance of fetching economic events
def test_fetch_economic_events_performance():
    """
    Test the performance of fetching economic events to ensure it completes within an acceptable time limit.
    """
    start_time = time.time()  # Record start time
    events = fetch_economic_events()  # Fetch economic events
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    # Check if the elapsed time is within the acceptable limit
    assert elapsed_time < FETCH_EVENTS_TIME_LIMIT, f"fetch_economic_events took {elapsed_time} seconds, exceeding the limit of {FETCH_EVENTS_TIME_LIMIT} seconds"
    assert isinstance(events, list)  # Ensure the result is a list
    assert len(events) > 0  # Ensure the list is not empty

# Test function for performance of storing events
def test_store_events_performance():
    """
    Test the performance of storing events to ensure it completes within an acceptable time limit.
    """
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
    start_time = time.time()  # Record start time
    store_events(test_events)  # Store the test events
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    # Check if the elapsed time is within the acceptable limit
    assert elapsed_time < STORE_EVENTS_TIME_LIMIT, f"store_events took {elapsed_time} seconds, exceeding the limit of {STORE_EVENTS_TIME_LIMIT} seconds"

# Test function for performance of retrieving events
def test_get_events_performance():
    """
    Test the performance of retrieving events to ensure it completes within an acceptable time limit.
    """
    start_time = time.time()  # Record start time
    events = get_events()  # Retrieve the events
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    # Check if the elapsed time is within the acceptable limit
    assert elapsed_time < GET_EVENTS_TIME_LIMIT, f"get_events took {elapsed_time} seconds, exceeding the limit of {GET_EVENTS_TIME_LIMIT} seconds"
    assert not events.empty  # Ensure the retrieved DataFrame is not empty

@pytest.mark.skipif(platform.system() != "Windows", reason="Email sending is only supported on Windows.")
def test_send_email_performance(mocker):
    """
    Test the performance of sending an email to ensure it completes within an acceptable time limit.
    """
    events_today = [
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
    recipient = "test@example.com"
    subject = "Test Email"
    message = "This is a test email."

    # Mock the Dispatch method from the win32com.client module
    mocker.patch('win32com.client.Dispatch')
    start_time = time.time()  # Record start time
    status = send_email(events_today, recipient, subject, message)  # Send the email
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    # Check if the elapsed time is within the acceptable limit
    assert elapsed_time < SEND_EMAIL_TIME_LIMIT, f"send_email took {elapsed_time} seconds, exceeding the limit of {SEND_EMAIL_TIME_LIMIT} seconds"
    assert status == "Email sent!"  # Ensure the email was sent successfully
