from datetime import datetime
import platform

if platform.system() == "Windows":
    import pythoncom
    import win32com.client as win32

    # Function to send an email with today's events
    def send_email(events_today, recipient, subject, message):
        """
        Sends an email with the list of today's economic events.
        
        Args:
            events_today (list): A list of dictionaries containing event details.
            recipient (str): The email address of the recipient.
            subject (str): The subject of the email.
            message (str): The custom message to be included in the email body.
            
        Returns:
            str: A success or failure message.
        """
        try:
            pythoncom.CoInitialize()  # Initialize COM for use with Outlook
            outlook = win32.Dispatch('outlook.application')  # Get the Outlook application object
            mail = outlook.CreateItem(0)  # Create a new mail item (email)
            mail.To = recipient  # Set the recipient of the email
            mail.Subject = subject  # Set the subject of the email

            # Create the HTML body of the email
            body_html = f"""
            <p>{message}</p>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 8px; text-align: left;">Date</th>
                    <th style="padding: 8px; text-align: left;">Time</th>
                    <th style="padding: 8px; text-align: left;">Currency</th>
                    <th style="padding: 8px; text-align: left;">Volatility</th>
                    <th style="padding: 8px; text-align: left;">Event</th>
                    <th style="padding: 8px; text-align: left;">Forecast</th>
                    <th style="padding: 8px; text-align: left;">Previous</th>
                </tr>
            """

            # Add each event to the HTML table
            for event in events_today:
                body_html += f"""
                <tr>
                    <td style="padding: 8px;">{event['Date']}</td>
                    <td style="padding: 8px;">{event['Time']}</td>
                    <td style="padding: 8px;">{event['Currency']}</td>
                    <td style="padding: 8px;">{event['Volatility']}</td>
                    <td style="padding: 8px;">{event['Event']}</td>
                    <td style="padding: 8px;">{event['Forecast']}</td>
                    <td style="padding: 8px;">{event['Previous']}</td>
                </tr>
                """

            body_html += """
            </table>
            <p>If you need additional information, please let us know.</p>
            <p>Best regards,<br>
            Your Team.</p>
            """

            mail.HTMLBody = body_html  # Set the HTML body of the email
            mail.Send()  # Send the email
            return "Email sent!"  # Return a success message
        except Exception as e:
            return f"Failed to send email: {e}"  # Return a failure message if an exception occurs
else:
    # Define a dummy function if not on Windows
    def send_email(events_today, recipient, subject, message):
        return "Email functionality is disabled in this environment."
