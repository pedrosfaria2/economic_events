import pytest
from data_fetcher import fetch_economic_events

def test_fetch_economic_events():
    events = fetch_economic_events()
    assert isinstance(events, list)
    assert len(events) > 0
    event = events[0]
    assert 'Date' in event
    assert 'Time' in event
    assert 'Currency' in event
    assert 'Volatility' in event
    assert 'Event' in event
    assert 'Forecast' in event
    assert 'Previous' in event
