import React, { useState } from "react";
import axios from "axios";

export default function FileUpload() {
    const [file, setFile] = useState(null);
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Please select a file first.");
            return;
        }

        setLoading(true);
        setError("");

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            setResponse(res.data);
        } catch (err) {
            setError("Error uploading file. Please try again.");
        }

        setLoading(false);
    };

    return (
        <div className="p-6 border-2 border-dashed rounded-lg bg-white shadow-lg">
            <h3 className="text-lg font-semibold mb-4">Upload Email File</h3>
            <input type="file" onChange={handleFileChange} className="w-full p-2 border rounded" accept=".eml" />
            
            <button
                onClick={handleUpload}
                className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
                disabled={loading}
            >
                {loading ? "Uploading..." : "Upload & Classify"}
            </button>

            {error && <p className="text-red-500 mt-4">{error}</p>}

            {response && (
                <div className="mt-6 p-4 border bg-white rounded">
                    <h2 className="text-lg font-bold mb-2">Classification Result</h2>
                    <p><strong>Status:</strong> {response.status ? "✅ Matched" : "❌ No Match Found"}</p>
                    <p><strong>Request Type:</strong> {response.request_type || "N/A"}</p>
                    <p><strong>Subrequest Types:</strong> {response.subrequest_types.length > 0 
                        ? response.subrequest_types.join(", ") 
                        : "N/A"}
                    </p>
                </div>
            )}
        </div>
    );
}
