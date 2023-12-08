import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def send_email(api_key, sender_email, recipient_email, subject, message):
    """
    Send an email using the SendGrid API.

    Parameters:
    - api_key (str): Your SendGrid API key.
    - sender_email (str): The email address from which the email will be sent.
    - recipient_email (str): The email address to which the email will be sent.
    - subject (str): The subject of the email.
    - message (str): The HTML content of the email.

    Returns:
    None: Prints success message or error message.

    Example:
    ```python
    api_key = 'your_sendgrid_api_key'
    sender_email = 'your_email@example.com'
    recipient_email = 'recipient@example.com'
    subject = 'Test Email Subject'
    message = '<p>This is a test email message.</p>'
    
    send_sendgrid_email(api_key, sender_email, recipient_email, subject, message)
    ```
    """
    # Create the SendGrid client
    sg = SendGridAPIClient(api_key)

    # Create the email content
    message = Mail(
        from_email=sender_email,
        to_emails=recipient_email,
        subject=subject,
        html_content=message
    )

    try:
        # Send the email
        response = sg.send(message)
        print(f'Success! Status code: {response.status_code}')
    except Exception as e:
        print(f'Error: {str(e)}')

# Example usage
api_key = os.getenv('email_api')
sender_email = 'info@remmittance.com'
recipient_email = 'rugema61@gmail.com'
subject = 'Testing'
message = '<p>Now reset password can be done with no issues. I am very happy</p>'

send_email(api_key, sender_email, recipient_email, subject, message)

