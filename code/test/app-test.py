import pytest
import os
from flask import Flask
from app import app  # Import the Flask app

@pytest.fixture
def client():
    """Flask test client setup."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_successful_email_processing(client):
    """Test successful email processing."""
    data = {
        "email_file": (open("test_email.eml", "rb"), "test_email.eml")
    }
    response = client.post("/process-email", data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert "email_subject" in json_data
    assert "classification_result" in json_data
    assert "processed_at" in json_data


def test_missing_email_file(client):
    """Test handling of missing email file."""
    response = client.post("/process-email", data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json()["error"] == "No email file provided"


def test_invalid_file_format(client):
    """Test handling of invalid file format."""
    data = {
        "email_file": (open("invalid_file.txt", "rb"), "invalid_file.txt")
    }
    response = client.post("/process-email", data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid file format. Only .eml files are supported"


def test_internal_server_error(client, mocker):
    """Test handling of unexpected errors."""
    mocker.patch("app.extract_email_content", side_effect=Exception("Test Error"))
    data = {
        "email_file": (open("test_email.eml", "rb"), "test_email.eml")
    }
    response = client.post("/process-email", data=data, content_type='multipart/form-data')
    
    assert response.status_code == 500
    assert "error" in response.get_json()
    assert response.get_json()["error"] == "Test Error"

if __name__ == "__main__":
    pytest.main()
