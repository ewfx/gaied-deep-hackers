import openai
import json
import re
from collections import OrderedDict
from config_loader import config

openai.api_key = config["OPENAI_API_KEY"]


def detect_duplicate(email_text):
    """
    Identifies if the email is a duplicate.
    - If the latest chain in a thread contains generic replies (e.g., "Thank you so much"), mark as duplicate.
    - If the thread has multiple detailed replies/forwards, do not mark as duplicate.
    """
    generic_reply_patterns = [
        r"thank you.*", r"thanks.*", r"appreciate it.*", r"noted.*",
        r"got it.*", r"acknowledged.*", r"understood.*"
    ]

    last_reply = email_text.strip().split("\n")[-1].lower()  # Get last line of email

    for pattern in generic_reply_patterns:
        if re.match(pattern, last_reply):
            return True  # Considered duplicate if generic response is detected

    return False  # Not a duplicate if it contains meaningful content


def assign_request(request_type, sub_request_type):
    """Assigns request to an appropriate person or team based on config."""
    roles_data = config["roles_and_skills"]

    if request_type in roles_data:
        if sub_request_type and isinstance(roles_data[request_type], dict):
            return roles_data[request_type].get(sub_request_type, {})
        return roles_data[request_type]  # Assign role/team if only RequestType exists

    return {"role": "Unassigned", "assigned_to": "General Support"}


def compute_from_model(email_subject, email_text, attachment_text=None):
    """Runs email classification using OpenAI with ordered response format and improved error handling."""
    try:
        classification_criteria = json.dumps(config["classification_criteria"], indent=4)
        extractable_fields = json.dumps(config["extractable_fields"], indent=4)

        # Detect duplicate based on generic responses in email thread
        is_duplicate = detect_duplicate(email_text)

        prompt = f"""
        You are an AI email classifier specializing in financial transactions.

        ### **Task**
        1. **Context-Based Classification:** Identify the **RequestType** and **SubRequestType**.  
        2. **Context-Based Data Extraction:** Extract relevant financial details based on **RequestType**.  
        3. **Priority Handling:** Prefer email content for classification, use attachments for numerical data.  
        4. **Duplicate Detection:** If latest response in thread contains generic text (e.g., "Thank you"), mark `"DuplicateFlag": true`.  
        5. **Assign Request:** Route the request to the appropriate **team or person**.  
        6. **Confidence Scoring:** Provide a **confidence score (0-100%)**.  

        ### **Classification Criteria**
        {classification_criteria}

        ### **Extractable Fields**
        {extractable_fields}

        ### **Email to Analyze**
        **Subject:** {email_subject}  
        **Email Content:** {email_text}  
        **Attachment Content:** {attachment_text or 'No Attachment'}

        ### **Expected JSON Response Format**
        You **must** return a **pure JSON** response with **no markdown formatting** or extra characters:
        {{
            "request_type": "<RequestType>",
            "sub_request_type": "<SubRequestType>",
            "DuplicateFlag": {str(is_duplicate).lower()},
            "confidence_score": "<Confidence Score in %>",
            "assigned_to": "<Team or Individual>",
            "role": "<Role Responsible>",
            "context": "<Explanation based on email and attachments>",
            "extracted_data": {{
                "<Relevant Field 1>": "<Value>",
                "<Relevant Field 2>": "<Value>"
            }}
        }}
        """

        client = openai.OpenAI()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an AI email classifier. Always respond in pure JSON format without markdown (` ``` `)."},
                {"role": "user", "content": prompt}
            ]
        )

        # ✅ Check if OpenAI response is empty or invalid
        if not response or not response.choices:
            return {"error": "OpenAI response is empty. Please check the API request or model output."}

        response_content = response.choices[0].message.content.strip()

        # ✅ Clean AI response (remove markdown artifacts)
        cleaned_response = response_content.replace("```json", "").replace("```", "").strip()

        # ✅ Log raw AI response for debugging
        print("Cleaned OpenAI Response:", cleaned_response)

        # ✅ Ensure AI response is valid JSON
        try:
            result = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse JSON from AI response: {str(e)}", "raw_response": cleaned_response}

        # Assign request to appropriate team/person
        assigned_data = assign_request(result.get("request_type"), result.get("sub_request_type"))
        result["assigned_to"] = assigned_data.get("assigned_to", "General Support")
        result["role"] = assigned_data.get("role", "Unassigned")

        # ✅ Convert result to an **OrderedDict** to enforce response order
        ordered_result = OrderedDict([
            ("request_type", result.get("request_type", "Unclassified")),
            ("sub_request_type", result.get("sub_request_type", "N/A")),
            ("DuplicateFlag", is_duplicate),
            ("confidence_score", result.get("confidence_score", "Unknown")),
            ("assigned_to", result.get("assigned_to")),
            ("role", result.get("role")),
            ("context", result.get("context", "No context provided")),
            ("extracted_data", result.get("extracted_data", {}))
        ])

        return ordered_result  # ✅ Returns a JSON response with correct order

    except Exception as e:
        return {"error": f"Error processing model request: {str(e)}"}
