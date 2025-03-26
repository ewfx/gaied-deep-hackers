### **📌 Email Classification - Hackathon Submission README**  

This README provides **step-by-step instructions** to set up, run, and test the **AI-powered Email Classification System** using OpenAI's **GPT-3.5-Turbo**. It includes folder structure, dependencies, API details, and troubleshooting tips.  

---

## **📌 Project Overview**  
This project is designed to classify emails by analyzing their content and extracting **request types, sub-request types, and confidence scores** using **AI-based classification**.

✔ **Upload & classify `.eml` or `.pdf` files**  
✔ **AI-powered request type detection**  
✔ **Extracts email content & attachments**  
✔ **User-friendly React UI with Flask API backend**  

---

## **📁 Folder Structure**
```
/email-classifier  
│── /backend             # Flask API  
│    ├── app.py          # Main Flask Application  
│    ├── ai_classifier.py   # AI classification logic  
│    ├── email_parser.py # Extracts email content & attachments  
|    |--- attachment_parser # Extracts text from PDFs, DOCX, and scanned PDFs with OCR
│    ├── email_reader.py      # Extracts text and attachments
│    ├── config.json     # Stores request type mappings & API keys  
│    ├── requirements.txt # Dependencies  
│── /frontend            # React Frontend  
│    ├── src  
│    │   ├── App.js       # Main React Component  
│    │   ├── UploadForm.js # File Upload & Classification  
│    │   ├── Dashboard.js # UI for displaying classification results  
│    │   ├── styles.css   # UI Styles  
|    |--  package.json
|    | -- tailwind.config.js
│── README.md            # Documentation  
```

---

## **🚀 Setup Instructions**

### **🔹 1. Clone the Repository**
```sh
git clone https://github.com/your-repo/email-classification.git  
cd email-classification  
```

---

### **🔹 2. Backend Setup (Flask API)**
```sh
cd backend  
python -m venv venv  
source venv/bin/activate  # Mac/Linux  
venv\Scripts\activate  # Windows  
pip install -r requirements.txt  
python app.py  
```
🔹 **Backend runs at:** `http://localhost:5000/`

---

### **🔹 3. Frontend Setup (React UI)**
```sh
cd frontend  
npm install  
npm start  
```
🔹 **Frontend runs at:** `http://localhost:3000/`

---

## **🔑 Setting Up API Keys**
To use **OpenAI GPT-3.5-Turbo** for classification, update `backend/config.py` with your API key.

```python
# backend/config.py
Open_API_KEY = "your-openai-api-key-here"
```

Then, restart your backend:
```sh
python app.py
```

---

## **📝 API Endpoints**

### **🔹 Upload Email File**
**Endpoint:** `POST /upload`  
Uploads an `.eml` or `.pdf` file and returns **classification, request type, and subrequest types**.

#### **Example Request (cURL)**
```sh
curl -X POST -F "file=@test_email.eml" http://localhost:5000/upload
```

#### **Example Response (JSON)**
```json
{
    "status": true,
    "request_type": "money movement - inbound",
    "subrequest_types": ["Inward Remittance"],
    "confidence_score": "85%"
}
```
If no request type is found:
```json
{
    "status": false,
    "request_type": null,
    "subrequest_types": []
}
```

---

## **📌 Tech Stack**

### **🔹 Frontend**
- **React.js** (UI)
- **Axios** (API calls)
- **Tailwind CSS** (Styling)

### **🔹 Backend**
- **Flask** (API)
- **Flask-CORS** (CORS handling)
- **OpenAI GPT-3.5-Turbo** (AI classification)
- **PDFPlumber** (Extracts PDFs from emails)
- **PyTesseract** (OCR for image attachments)

---

## **🛠️ Dependencies (`requirements.txt`)**
```
Flask
flask-cors
openai
PyPDF2
python-docx
pymupdf  # PyMuPDF
pytesseract
Pillow
email-validator
```
📌 **Install with:**  
```sh
pip install -r requirements.txt
```

---

## **🚀 How to Use the UI**
1. **Run Backend (`python app.py`) & Frontend (`npm start`)**  
2. **Go to:** `http://localhost:3000/`  
3. **Upload `.eml` File** (Email Format)  
4. **Click "Upload & Classify"**  
5. **See Classification Results in UI** 🎯  

---

## **🛠️ Troubleshooting**
🔹 **Backend Not Starting?**
```sh
pip install flask flask-cors
```
🔹 **Frontend Not Loading?**
```sh
npm install
```

---

## **📜 License**
📌 Open-source under the **MIT License**.

