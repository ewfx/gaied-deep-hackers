import os
from email import policy
from email.parser import BytesParser
from config_loader import config

def extract_email_content(eml_file):
    """Extracts text and attachments from a .eml email file."""
    try:
        with open(eml_file, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        email_subject = msg["subject"]
        email_body = msg.get_body(preferencelist=("plain", "html")).get_content() if msg.get_body() else ""

        attachment_dir = config["attachments_dir"]
        os.makedirs(attachment_dir, exist_ok=True)
        extracted_attachments = []

        for part in msg.iter_attachments():
            attachment_path = os.path.join(attachment_dir, part.get_filename())
            with open(attachment_path, "wb") as f:
                f.write(part.get_payload(decode=True))
            extracted_attachments.append(attachment_path)

        return f"Subject: {email_subject}\nBody: {email_body}", extracted_attachments

    except Exception as e:
        return f"Error extracting email content: {str(e)}", []
