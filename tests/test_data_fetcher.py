import pytest
from data_fetcher import fetch_economic_events

# Test function for fetching economic events
def test_fetch_economic_events():
    """
    Test the fetch_economic_events function to ensure it correctly fetches economic events.

    This test checks the following:
    1. The function returns a list.
    2. The list is not empty.
    3. The first event in the list contains the expected keys: 'Date', 'Time', 'Currency', 'Volatility', 'Event', 'Forecast', and 'Previous'.
    """
    # Fetch economic events
    events = fetch_economic_events()

    # Assert that the result is a list
    assert isinstance(events, list)

    # Assert that the list is not empty
    assert len(events) > 0

    # Assert that the first event in the list contains the expected keys
    event = events[0]
    assert 'Date' in event
    assert 'Time' in event
    assert 'Currency' in event
    assert 'Volatility' in event
    assert 'Event' in event
    assert 'Forecast' in event
    assert 'Previous' in event

def test_fetch_economic_events_network_error(mocker):
    """
    Test the fetch_economic_events function to handle network errors gracefully.

    This test checks the following:
    1. The httpx.Client.post method is mocked to raise an Exception simulating a network error.
    2. The fetch_economic_events function should return an empty list when a network error occurs.
    """
    # Mock the httpx.Client.post method to raise an Exception with the message "Network Error"
    mocker.patch('httpx.Client.post', side_effect=Exception("Network Error"))

    # Fetch economic events
    events = fetch_economic_events()

    # Assert that the function returns an empty list in case of a network error
    assert events == []
