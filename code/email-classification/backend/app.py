from flask import Flask, request, jsonify
from email_parser import extract_email_content
from classifier import classify_email, validate_request_type
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load config
with open("config.json") as f:
    config = json.load(f)

@app.route("/upload", methods=["POST"])
def upload_email():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    content, attachments = extract_email_content(file)

    # Validate against config.json
    status, request_type, subrequest_types = validate_request_type(content, attachments)

    return jsonify({
        "status": status,
        "request_type": request_type,
        "subrequest_types": subrequest_types
    })

if __name__ == "__main__":
    app.run(debug=True)
