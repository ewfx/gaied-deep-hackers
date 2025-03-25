import email
import os
from werkzeug.utils import secure_filename

def extract_email_content(file):
    """
    Extracts the content and attachment names from an .eml email file.
    
    Returns:
        - Email body as text
        - List of attachment names
    """
    content = ""
    attachments = []
    
    # Parse the email
    msg = email.message_from_bytes(file.read())

    # Extract the email body
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                content += part.get_payload(decode=True).decode(errors="ignore")
            elif part.get_filename():  # Extract attachment names
                attachments.append(secure_filename(part.get_filename()))
    else:
        content = msg.get_payload(decode=True).decode(errors="ignore")

    return content, attachments
