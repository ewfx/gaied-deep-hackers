import PyPDF2
import docx
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from config_loader import config

# Set up Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = config["TESSERACT_PATH"]

def extract_text_from_attachment(attachment_path):
    """Extracts text from PDFs, DOCX, and scanned PDFs with OCR."""
    try:
        text = ""
        if attachment_path.endswith(".pdf"):
            with open(attachment_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                extracted_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

                if extracted_text.strip():
                    text = extracted_text
                else:
                    text = extract_images_from_pdf(attachment_path)

        elif attachment_path.endswith(".docx"):
            doc = docx.Document(attachment_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        else:
            text = "Unsupported file format"
        return text

    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_images_from_pdf(pdf_path):
    """Extracts images from a PDF and applies OCR."""
    try:
        doc = fitz.open(pdf_path)
        extracted_text = ""

        for page_num in range(len(doc)):
            for img_index, img in enumerate(doc[page_num].get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                text = pytesseract.image_to_string(image)
                extracted_text += f"\n[Page {page_num + 1}, Image {img_index + 1}]:\n{text}\n"

        return extracted_text

    except Exception as e:
        return f"Error extracting image text: {str(e)}"
