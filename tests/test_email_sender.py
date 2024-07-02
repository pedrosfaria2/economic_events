import pytest
from email_sender import send_email

def test_send_email(mocker):
    # Define a list of events for the test email
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
    # Define the recipient, subject, and message for the test email
    recipient = "test@example.com"
    subject = "Test Email"
    message = "This is a test email."

    # Mock the Dispatch method from the win32com.client module
    mock_dispatch = mocker.patch('win32com.client.Dispatch')
    
    # Call the send_email function with the test data
    status = send_email(events_today, recipient, subject, message)
    
    # Assert that the send_email function returns the expected status
    assert status == "Email sent!"
    
    # Assert that the Dispatch method was called exactly once
    mock_dispatch.assert_called_once()
