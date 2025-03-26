from flask import Flask, request, jsonify
import os
from datetime import datetime
from email_reader import extract_email_content
from attachment_parser import extract_text_from_attachment
from ai_classifier import compute_from_model
from file_handler import (
    load_seen_hashes, save_seen_hashes,
    load_processed_emails, save_processed_email
)

app = Flask(__name__)

@app.route("/process-email", methods=["POST"])
def process_email():
    """Processes an uploaded .eml file, checks for duplicates, and stores results."""
    try:

        if "email_file" not in request.files:
            return jsonify({"error": "No email file provided"}), 400

        eml_file = request.files["email_file"]
        if not eml_file.filename.endswith(".eml"):
            return jsonify({"error": "Invalid file format. Only .eml files are supported"}), 400

        # Save temp file
        file_path = f"temp_{eml_file.filename}"
        eml_file.save(file_path)

        # Extract email content & attachments
        email_text, attachments = extract_email_content(file_path)
        email_subject = email_text.split("\n")[0].replace("Subject: ", "").strip()


        # Extract text from attachments
        attachment_texts = [extract_text_from_attachment(att) for att in attachments]
        combined_attachment_text = "\n".join(attachment_texts)

        # **Process email using AI model**
        classification_result = compute_from_model(email_subject, email_text, combined_attachment_text)

        # **Store processed email**
        email_data = {
            "email_subject": email_subject,
            "classification_result": classification_result,
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # **Cleanup temp files**
        os.remove(file_path)
        for att in attachments:
            os.remove(att)

        return jsonify(email_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
