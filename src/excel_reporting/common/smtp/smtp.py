import smtplib

from os import getenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(message: MIMEMultipart) -> None:
    _smtp_server: str = getenv("XLR_SMTP_SERVER", "")
    _smtp_port: int = int(getenv("XLR_SMTP_PORT", 587))
    _smtp_sender_login: str = getenv("XLR_SMTP_SENDER_LOGIN", "")
    _smtp_sender_password: str = getenv("XLR_SMTP_SENDER_PASSWORD", "")

    try:
        assert _smtp_server, "XLR_SMTP_SERVER environment variable is not set."
        assert _smtp_sender_login, "XLR_SMTP_SENDER_LOGIN environment variable is not set."
        assert _smtp_sender_password, "XLR_SMTP_SENDER_PASSWORD environment variable is not set."

        with smtplib.SMTP(_smtp_server, _smtp_port) as server:
            server.starttls()
            server.login(_smtp_sender_login, _smtp_sender_password)
            server.send_message(message)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e
