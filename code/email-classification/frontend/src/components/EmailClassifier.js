import React, { useState } from "react";

const EmailClassifier = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an .eml file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/classify-email", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setResult(data);
        setError(null);
      } else {
        setError(data.error || "Failed to classify email.");
      }
    } catch (error) {
      setError("Error connecting to the server.");
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-bold mb-4">Email Classification</h2>
      <input type="file" accept=".eml" onChange={handleFileChange} className="mb-4" />
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
      >
        Upload & Classify
      </button>
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded-md">
          <h3 className="font-semibold">Classification Result:</h3>
          <p><strong>Request Type:</strong> {result.request_type}</p>
          <p><strong>Subrequest Type:</strong> {result.subrequest_type}</p>
          <p><strong>Classification:</strong> {result.classification}</p>
          <p><strong>Attachments Verified:</strong> {result.attachments_verified ? "Yes" : "No"}</p>
        </div>
      )}
    </div>
  );
};

export default EmailClassifier;
