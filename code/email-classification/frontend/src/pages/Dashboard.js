import React, { useState } from "react";
import FileUpload from "../components/FileUpload";
import EmailList from "../components/EmailList";

export default function Dashboard() {
    const [uploadedEmails, setUploadedEmails] = useState([]);

    const handleNewUpload = (data) => {
        setUploadedEmails([...uploadedEmails, {
            subject: `Email - ${uploadedEmails.length + 1}`,
            status: data.status ? "Processed" : "No Match Found",
        }]);
    };

    return (
        <div className="p-6">
            <h2 className="text-2xl font-semibold">Dashboard</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                <FileUpload onUpload={handleNewUpload} />
                <EmailList uploadedEmails={uploadedEmails} />
            </div>
        </div>
    );
}
