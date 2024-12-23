import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st

# Email configuration
sender_email = st.secrets["GMAIL"]["sender_email"]

# SMTP server configuration
smtp_server = st.secrets["GMAIL"]["smtp_server"]
smtp_port = st.secrets["GMAIL"]["smtp_port"]
smtp_username = st.secrets["GMAIL"]["smtp_username"]
smtp_password = st.secrets["GMAIL"]["smtp_password"]


def send_email_with_password(mail_adress, password):
    receiver_email = mail_adress
    subject = "Pasword Requested"
    body = f"Your new password is: {password}"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    # msg.attach(MIMEText(password, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        return True

    except Exception:
        print(traceback.format_exc())
        return False

    finally:
        # Close the connection
        server.quit()