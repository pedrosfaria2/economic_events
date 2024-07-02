import pytest
from email_sender import send_email

def test_send_email(mocker):
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

    mock_dispatch = mocker.patch('win32com.client.Dispatch')
    status = send_email(events_today, recipient, subject, message)
    assert status == "Email sent!"
    mock_dispatch.assert_called_once()
