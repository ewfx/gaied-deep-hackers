import os
import json
from config_loader import config

PROCESSED_FILE = config["processed_emails_file"]
SEEN_HASHES_FILE = config["seen_hashes_file"]

def load_seen_hashes():
    """Loads seen email subjects to prevent duplicate processing."""
    if os.path.exists(SEEN_HASHES_FILE):
        with open(SEEN_HASHES_FILE, "r") as file:
            return set(json.load(file))
    return set()

def save_seen_hashes(seen_hashes):
    """Saves seen email subjects to track processed emails."""
    with open(SEEN_HASHES_FILE, "w") as file:
        json.dump(list(seen_hashes), file)

def load_processed_emails():
    """Loads existing processed emails if the file exists."""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_processed_email(email_data):
    """Saves processed email results to JSON file."""
    processed_emails = load_processed_emails()
    processed_emails.append(email_data)

    with open(PROCESSED_FILE, "w") as file:
        json.dump(processed_emails, file, indent=4)
