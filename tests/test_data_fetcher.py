import pytest
from data_fetcher import fetch_economic_events

# Test function for fetching economic events
def test_fetch_economic_events():
    # Call the fetch_economic_events function to retrieve events
    events = fetch_economic_events()

    # Check if the returned value is a list
    assert isinstance(events, list)

    # Check if the list is not empty
    assert len(events) > 0

    # Check if the first event in the list contains the expected keys
    event = events[0]
    assert 'Date' in event
    assert 'Time' in event
    assert 'Currency' in event
    assert 'Volatility' in event
    assert 'Event' in event
    assert 'Forecast' in event
    assert 'Previous' in event
