import React, { useState, useRef } from "react";
import axios from "axios";

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showJson, setShowJson] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setResponse(null);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }

    setError("");
    setLoading(true);

    const formData = new FormData();
    formData.append("email_file", file);

    try {
      const res = await axios.post("http://localhost:5000/process-email", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("✅ API Response:", res.data);

      if (res.data.error) {
        throw new Error(res.data.error);
      }

      // Filter out empty values and "N/A" from extracted_data
      const filteredExtractedData = Object.fromEntries(
        Object.entries(res.data.classification_result.extracted_data || {}).filter(
          ([_, value]) => value && value !== "N/A"
        )
      );

      setResponse({
        ...res.data.classification_result,
        extracted_data: filteredExtractedData,
        email_subject: res.data.email_subject,
        processed_at: res.data.processed_at,
      });
    } catch (err) {
      console.error("❌ Upload Error:", err);
      setError(err.message || "Error uploading file. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setResponse(null);
    setError("");
    setShowJson(false);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleCopyJson = () => {
    if (response) {
      navigator.clipboard.writeText(JSON.stringify(response, null, 2));
      alert("✅ JSON copied to clipboard!");
    }
  };

  return (
    <div className="p-6 bg-white shadow-lg rounded-md w-3/4 mx-auto">
      <h2 className="text-xl font-bold mb-4">Upload Email for Classification</h2>

      <input type="file" ref={fileInputRef} onChange={handleFileChange} className="border p-2 rounded w-full" />

      <div className="flex gap-4 mt-4">
        <button
          onClick={handleUpload}
          className={`px-4 py-2 rounded ${file ? "bg-blue-500 hover:bg-blue-600 text-white" : "bg-gray-300 text-gray-600 cursor-not-allowed"}`}
          disabled={!file || loading}
        >
          {loading ? "Uploading..." : "Upload & Classify"}
        </button>

        <button
          onClick={handleReset}
          className={`px-4 py-2 rounded ${response || error ? "bg-gray-400 hover:bg-gray-500 text-white" : "bg-gray-300 text-gray-600 cursor-not-allowed"}`}
          disabled={!response && !error}
        >
          Reset
        </button>
      </div>

      {error && <p className="text-red-500 mt-2">❌ {error}</p>}

      {response && (
        <div className="mt-6 p-4 bg-gray-100 border rounded">
          <h3 className="text-lg font-semibold text-blue-600">📩 Email Classification Result:</h3>

          <p><strong>📌 Subject:</strong> {response.email_subject}</p>
          <p><strong>📅 Processed At:</strong> {response.processed_at}</p>
          <p><strong>🔹 Request Type:</strong> {response.request_type}</p>
          <p><strong>🔸 Subrequest Type:</strong> {response.sub_request_type}</p>

          <p className={`mt-2 font-semibold ${response.DuplicateFlag ? "text-red-600" : "text-green-600"}`}>
            {response.DuplicateFlag ? "🔁 Duplicate Email" : "✅ Unique Email"}
          </p>

          <p className="mt-2"><strong>👤 Assigned To:</strong> {response.assigned_to} ({response.role})</p>
          <p className="mt-2"><strong>🎯 Confidence Score:</strong> {response.confidence_score}</p>

          {response.context && (
            <p className="mt-2"><strong>📖 Context:</strong> {response.context}</p>
          )}

          {Object.keys(response.extracted_data).length > 0 && (
            <>
              <h3 className="text-lg font-semibold text-blue-600 mt-4">📋 Extracted Details:</h3>
              <table className="w-full mt-2 border-collapse border border-gray-400">
                <thead>
                  <tr className="bg-gray-200">
                    <th className="border border-gray-400 p-2 text-left">Field</th>
                    <th className="border border-gray-400 p-2 text-left">Value</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(response.extracted_data).map(([key, value]) => (
                    <tr key={key} className="border border-gray-400">
                      <td className="border border-gray-400 p-2">{key}</td>
                      <td className="border border-gray-400 p-2">{value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}

          {/* Collapsible JSON Response */}
          <button
            onClick={() => setShowJson(!showJson)}
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
          >
            {showJson ? "Hide JSON Response" : "Show Full JSON Response"}
          </button>

          {showJson && (
            <div className="mt-4 p-4 bg-gray-200 rounded">
              <h3 className="font-semibold">📜 Full JSON Response:</h3>
              <pre className="w-full h-40 p-2 border rounded bg-white font-mono text-sm overflow-auto">
                {JSON.stringify(response, null, 2)}
              </pre>
              <button
                onClick={handleCopyJson}
                className="mt-2 bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
              >
                📋 Copy JSON
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default UploadForm;
