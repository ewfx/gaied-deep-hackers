import React, { useState } from "react";
import axios from "axios";

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }
    
    setError(""); // Clear previous errors
    setLoading(true);
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("API Response:", res.data); // Debugging
      setResponse(res.data);
    } catch (error) {
      setError("Error uploading file. Please try again.");
      console.error("Upload Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white shadow-lg rounded-md w-3/4 mx-auto">
      <h2 className="text-xl font-bold mb-4">Upload Email for Classification</h2>

      <input type="file" onChange={handleFileChange} className="border p-2 rounded w-full" />
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 mt-4 rounded"
        disabled={loading}
      >
        {loading ? "Uploading..." : "Upload & Classify"}
      </button>

      {error && <p className="text-red-500 mt-2">{error}</p>}

      {response && (
        <div className="mt-6 p-4 bg-gray-100 border rounded">
          <h3 className="text-lg font-semibold text-blue-600">Classification Result:</h3>
          <p><strong>Status:</strong> {response.status ? "✅ Found" : "❌ Not Found"}</p>
          <p><strong>Request Type:</strong> {response.request_type || "None"}</p>
          <p><strong>Subrequest Types:</strong> {response.subrequest_types.length > 0 ? response.subrequest_types.join(", ") : "None"}</p>

          <h3 className="text-lg font-semibold text-blue-600 mt-4">Extracted Content:</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{response.content}</p>
        </div>
      )}
    </div>
  );
};

export default UploadForm;
