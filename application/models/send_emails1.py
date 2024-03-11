import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration settings
sender_email = "info@remmittance.com"
receiver_email = "rugema61@gmail.com"
password = "Shami@2020"  # Use the email account's password
smtp_server = "mail.remmittance.com"
smtp_port = 465  # SMTP port for SSL/TLS

# Create a multipart message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Test email from Python"

# Add body to email
body = "This is a test email sent from Python using SSL/TLS settings."
message.attach(MIMEText(body, "plain"))

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

