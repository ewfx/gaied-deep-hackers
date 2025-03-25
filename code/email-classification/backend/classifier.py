import google.generativeai as genai
import json
from config import GOOGLE_API_KEY

# Configure Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)

# Load config
with open("config.json") as f:
    config = json.load(f)

def classify_email(content):
    model = genai.GenerativeModel("gemini-1.5-pro")  
    response = model.generate_content(f"Classify this email: {content}")
    return response.text

def validate_request_type(content, attachments):
    request_type_found = None
    subrequest_types_found = []

    # Normalize text for better matching
    content_lower = content.lower()
    attachments_lower = [att.lower() for att in attachments]

    for request_type, subrequests in config["request_type_mapping"].items():
        for subrequest in subrequests:
            subrequest_lower = subrequest.lower()

            # Check in email body
            if subrequest_lower in content_lower:
                request_type_found = request_type
                subrequest_types_found.append(subrequest)

            # Check in attachments
            for attachment in attachments_lower:
                if subrequest_lower in attachment:
                    request_type_found = request_type
                    subrequest_types_found.append(subrequest)

    status = bool(request_type_found)  # True if found, False otherwise
    return status, request_type_found, list(set(subrequest_types_found))  # Remove duplicates
