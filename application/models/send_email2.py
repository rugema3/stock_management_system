import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender_email, receiver_email, password, smtp_server, smtp_port, subject, html_message):
    """
    Send an email with HTML content using SMTP.

    Args:
        sender_email (str): The sender's email address.
        receiver_email (str): The recipient's email address.
        password (str): The password for the sender's email account.
        smtp_server (str): The SMTP server address.
        smtp_port (int): The SMTP port number.
        subject (str): The subject of the email.
        html_message (str): The HTML content of the email message.

    Returns:
        None

    Raises:
        Exception: If an error occurs while sending the email.

    """
    # Connect to SMTP server
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_email, password)

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach HTML message
    message.attach(MIMEText(html_message, "html"))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        server.quit()  # Close the connection

if __name__ == '__main__':

    # Email configuration settings
    sender_email = "info@remmittance.com"
    receiver_email = "rugema61@gmail.com"
    password = "Shami@2020"  # Use the email account's password
    smtp_server = "mail.remmittance.com"
    smtp_port = 465  # SMTP port for SSL/TLS

    # HTML message
    html_message = """
    <html>
    <body>
    <h1>This is a test email sent from Python using SSL/TLS settings.</h1>
    <p>Hello, World!</p>
    </body>
    </html>
    """

    # Call the send_email function with the provided configuration settings and HTML message
    subject = "Test email from Python"
    send_email(sender_email, receiver_email, password, smtp_server, smtp_port, subject, html_message)
