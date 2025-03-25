### **📌 Updated & Structured README for Your Email Classification Project**  

This README provides **step-by-step instructions** to set up, run, and test your **Email Classification AI** project. It includes **folder structure, dependencies, API details, and troubleshooting tips**.  

---

## **📌 Project Overview**  
This AI-powered **Email Classification System** extracts email content and attachments, identifies request types, and classifies emails using **Google Gemini AI** or open-source LLM models.  

✔ **Upload & classify `.eml` files**  
✔ **AI-powered request type detection**  
✔ **Extracts email content & attachments**  
✔ **Simple React UI with Flask API backend**  

---

## **📁 Folder Structure**
```
/email-classification  
│── /backend             # Flask API  
│    ├── app.py          # Main Flask Application  
│    ├── classifier.py   # AI classification logic  
│    ├── email_parser.py # Extracts email content & attachments  
│    ├── config.py       # Stores API keys & configuration  
│    ├── config.json     # Stores request type mappings  
│    ├── requirements.txt # Dependencies  
│── /frontend            # React Frontend  
│    ├── src  
│    │   ├── App.js       # Main React Component  
│    │   ├── UploadForm.js # File Upload & Classification  
│    │   ├── Dashboard.js # Main UI for Classification  
│    │   ├── styles.css   # UI Styles  
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

## **🔑 Setting Up Your Google API Key**
To use **Google Gemini AI** for classification, you need to set up your API key in `backend/config.py`.  

### **1️⃣ Generate a Google API Key**
1. **Go to the Google AI Console:**  
   - Open **[Google AI Developer Console](https://ai.google.dev/)**  
   - Sign in with your **Google Account**.  

2. **Create a new API Key:**  
   - Click on **"Get API Key"**.  
   - Follow the instructions and copy your API key.  

3. **Enable the Gemini AI API (if required):**  
   - Go to **Google Cloud Console**: [https://console.cloud.google.com/](https://console.cloud.google.com/)  
   - Navigate to **API & Services > Library**.  
   - Search for **"Generative AI API"** and enable it.  

### **2️⃣ Add Your API Key in `config.py`**
Create or update `backend/config.py` with:
```python
# backend/config.py
GOOGLE_API_KEY = "your-google-api-key-here"
```

### **3️⃣ Restart Your Backend**
```sh
python app.py
```

---

## **📝 API Endpoints**
### **🔹 Upload Email File**
**Endpoint:** `POST /upload`  
Uploads an `.eml` file and returns **classification, request type, and subrequest types**.  

#### **Example Request (cURL)**
```sh
curl -X POST -F "file=@test_email.eml" http://localhost:5000/upload
```

#### **Example Response (JSON)**
```json
{
    "status": true,
    "request_type": "money movement - inbound",
    "subrequest_types": ["Inward Remittance"]
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
- **Google Gemini AI** (LLM Classification)
- **PDFPlumber** (Extracts PDFs from emails)
- **PyTesseract** (OCR for image attachments)

---

## **🛠️ Dependencies (`requirements.txt`)**
```
flask
flask-cors
pdfplumber
pytesseract
transformers
torch
google-generativeai
email
openai
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


