import pytest
from email_sender import send_email
import platform

@pytest.mark.skipif(platform.system() != "Windows", reason="Email sending is only supported on Windows.")
def test_send_email(mocker):
    """
    Test the send_email function to ensure it sends an email successfully.

    This test checks if the send_email function can send an email with the given events,
    recipient, subject, and message. It uses the mocker library to mock the Dispatch method
    from the win32com.client module to avoid sending a real email during the test.
    """
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

@pytest.mark.skipif(platform.system() != "Windows", reason="Email sending is only supported on Windows.")
def test_send_email_dispatch_error(mocker):
    """
    Test the send_email function to ensure it handles dispatch errors correctly.

    This test checks if the send_email function can handle errors when the Dispatch method
    from the win32com.client module raises an exception. It uses the mocker library to mock
    the Dispatch method to raise an exception and verifies if the function handles it properly.
    """
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

    # Mock the Dispatch method to raise an exception
    mock_dispatch = mocker.patch('win32com.client.Dispatch', side_effect=Exception("Dispatch Error"))
    
    # Call the send_email function with the test data
    status = send_email(events_today, recipient, subject, message)
    
    # Assert that the send_email function returns the expected error message
    assert status == "Failed to send email: Dispatch Error"
    
    # Assert that the Dispatch method was called exactly once
    mock_dispatch.assert_called_once()

@pytest.mark.skipif(platform.system() == "Windows", reason="This test is only valid on non-Windows platforms.")
def test_send_email_non_windows():
    """
    Test the send_email function to ensure it returns the correct message when not on Windows.

    This test checks if the send_email function returns the correct message when it is not
    running on a Windows platform.
    """
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

    # Call the send_email function with the test data
    status = send_email(events_today, recipient, subject, message)
    
    # Assert that the send_email function returns the expected message for non-Windows platforms
    assert status == "Email sending is only supported on Windows."
