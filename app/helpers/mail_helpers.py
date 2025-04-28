from flask_mail import Message
from app.extensions import mail
from app.config import Config
from flask import current_app as app

def send_mail(subject=None, sender=None, recipients=[], body=None): 
    message:Message = Message(
        subject=subject or f"{Config.APP_NAME}",
        sender=sender or Config.MAIL_DEFAULT_SENDER,  # Use the default sender from config
        recipients=recipients,  # List of recipient email addresses
        body=body
    )
    mail.send(message=message)
