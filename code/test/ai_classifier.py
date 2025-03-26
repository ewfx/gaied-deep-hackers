import pytest
import json
from unittest.mock import patch
from ai_classifier import compute_from_model, detect_duplicate, assign_request


def test_detect_duplicate():
    """Test detection of duplicate email responses."""
    assert detect_duplicate("Thank you for your response.") is True
    assert detect_duplicate("Got it. Appreciated!") is True
    assert detect_duplicate("Here is the requested information.") is False
    assert detect_duplicate("Please see the attached file.") is False


def test_assign_request():
    """Test assignment of request based on config mappings."""
    with patch("ai_classifier.config", {"roles_and_skills": {
        "Fee Payment": {"Letter of Credit Fee": {"role": "Trade Finance Expert", "assigned_to": "Trade Finance Team"}},
        "General Inquiry": {"role": "Support Specialist", "assigned_to": "Support Team"}
    }}):
        
        assert assign_request("Fee Payment", "Letter of Credit Fee") == {
            "role": "Trade Finance Expert", "assigned_to": "Trade Finance Team"
        }
        
        assert assign_request("General Inquiry", None) == {
            "role": "Support Specialist", "assigned_to": "Support Team"
        }
        
        assert assign_request("Unknown Request", None) == {
            "role": "Unassigned", "assigned_to": "General Support"
        }


def test_compute_from_model():
    """Test AI classification with mocked OpenAI response."""
    mock_response = {
        "request_type": "Fee Payment",
        "sub_request_type": "Letter of Credit Fee",
        "DuplicateFlag": False,
        "confidence_score": "90%",
        "assigned_to": "Trade Finance Team",
        "role": "Trade Finance Expert",
        "context": "Identified as a fee payment request.",
        "extracted_data": {"Amount": "$5000"}
    }
    
    with patch("ai_classifier.openai.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value.choices = [
            type("", (object,), {"message": type("", (object,), {"content": json.dumps(mock_response)})()})()
        ]
        
        result = compute_from_model("Invoice Payment", "Please process the $5000 payment.")
        assert result["request_type"] == "Fee Payment"
        assert result["sub_request_type"] == "Letter of Credit Fee"
        assert result["DuplicateFlag"] is False
        assert result["confidence_score"] == "90%"
        assert result["assigned_to"] == "Trade Finance Team"
        assert result["role"] == "Trade Finance Expert"
        assert "Amount" in result["extracted_data"]


def test_compute_from_model_invalid_json():
    """Test handling of invalid JSON response from OpenAI."""
    with patch("ai_classifier.openai.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value.choices = [
            type("", (object,), {"message": type("", (object,), {"content": "Invalid JSON"})()})()
        ]
        
        result = compute_from_model("Test Subject", "Test Content")
        assert "error" in result
        assert "Failed to parse JSON" in result["error"]

if __name__ == "__main__":
    pytest.main()
