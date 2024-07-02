import pytest
import time
from data_fetcher import fetch_economic_events
from data_storer import store_events, get_events
from email_sender import send_email

# Define the acceptable time limits in seconds
FETCH_EVENTS_TIME_LIMIT = 10
STORE_EVENTS_TIME_LIMIT = 2
GET_EVENTS_TIME_LIMIT = 2
SEND_EMAIL_TIME_LIMIT = 2

# Benchmark for fetching economic events
def test_fetch_economic_events_benchmark(benchmark):
    result = benchmark.pedantic(fetch_economic_events, iterations=1, rounds=5)
    assert isinstance(result, list)
    assert len(result) > 0

# Benchmark for storing events
def test_store_events_benchmark(benchmark):
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
    benchmark(store_events, test_events)

# Benchmark for getting events
def test_get_events_benchmark(benchmark):
    result = benchmark(get_events)
    assert not result.empty
    assert len(result) > 0

# Benchmark for sending email
def test_send_email_benchmark(mocker, benchmark):
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
    recipient = "test@example.com"
    subject = "Test Email"
    message = "This is a test email."

    mock_dispatch = mocker.patch('win32com.client.Dispatch')
    
    # Benchmark the send_email function with a single iteration
    def send_email_once():
        return send_email(test_events, recipient, subject, message)
    
    status = benchmark.pedantic(send_email_once, iterations=1, rounds=1)
    assert status == "Email sent!"
    mock_dispatch.assert_called_once()
