import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.http import HttpResponse

def send_custom_email(request, receiver_email, topic, message):
    # Set the email subject and body to the provided topic and message
    subject = topic
    body = message

    # Create MIMEText object with the body text and charset
    body_mime = MIMEText(body, 'plain', 'utf-8')

    # Construct the email with headers and body
    email_msg = MIMEMultipart()
    email_msg['Subject'] = subject
    email_msg['From'] = settings.EMAIL_HOST_USER
    email_msg['To'] = receiver_email  # Set the receiver's email address
    email_msg.attach(body_mime)

    # Create the SSL context for a secure connection
    ssl_context = ssl.create_default_context()

    # Connect to the SMTP server, secure the connection, login, and send the email
    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as connection:
        connection.starttls(context=ssl_context)  # Secure the connection with TLS
        connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # Perform SMTP authentication
        connection.send_message(email_msg)  # Send the email to the receiver

    print("Email sent successfully to", receiver_email)

    # Return an HttpResponse indicating success
    return HttpResponse("Email sent successfully.")