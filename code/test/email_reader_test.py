import pytest
import os
from email.parser import BytesParser
from email.policy import default
from extract_email_content import extract_email_content  # Import function from your module

def create_test_eml(file_path, subject="Test Email", body="This is a test email.", attachment_name=None, attachment_content=b"Test attachment"):
    """Creates a sample .eml file for testing."""
    from email.message import EmailMessage
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg.set_content(body)
    
    if attachment_name:
        msg.add_attachment(attachment_content, maintype='application', subtype='octet-stream', filename=attachment_name)
    
    with open(file_path, "wb") as f:
        f.write(msg.as_bytes())

test_eml_file = "test_email.eml"

@pytest.fixture
def setup_eml_file():
    """Fixture to create and clean up a test .eml file."""
    create_test_eml(test_eml_file)
    yield test_eml_file
    os.remove(test_eml_file)

def test_extract_email_content(setup_eml_file):
    """Test extracting email content from a valid .eml file."""
    email_text, attachments = extract_email_content(setup_eml_file)
    assert "Subject: Test Email" in email_text
    assert "Body: This is a test email." in email_text
    assert len(attachments) == 0  # No attachments in this case

def test_extract_email_with_attachment():
    """Test extracting email with an attachment."""
    attachment_name = "test_attachment.txt"
    attachment_content = b"This is attachment content."
    test_eml_with_attachment = "test_email_with_attachment.eml"
    
    create_test_eml(test_eml_with_attachment, attachment_name=attachment_name, attachment_content=attachment_content)
    
    email_text, attachments = extract_email_content(test_eml_with_attachment)
    assert "Subject: Test Email" in email_text
    assert "Body: This is a test email." in email_text
    assert len(attachments) == 1
    assert os.path.exists(attachments[0])  # Ensure attachment file was created
    
    # Cleanup
    os.remove(test_eml_with_attachment)
    os.remove(attachments[0])

def test_invalid_file():
    """Test handling of an invalid .eml file."""
    invalid_file = "invalid.eml"
    with open(invalid_file, "w") as f:
        f.write("This is not a valid email file.")
    
    email_text, attachments = extract_email_content(invalid_file)
    assert "Error extracting email content" in email_text
    assert len(attachments) == 0
    
    os.remove(invalid_file)

if __name__ == "__main__":
    pytest.main()
