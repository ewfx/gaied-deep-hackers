import React, { useEffect, useState } from "react";

export default function EmailList({ uploadedEmails }) {
    return (
        <div className="p-6 bg-white rounded-lg shadow-lg">
            <h3 className="text-lg font-semibold mb-4">Processed Emails</h3>
            {uploadedEmails.length === 0 ? (
                <p>No processed emails yet.</p>
            ) : (
                <ul>
                    {uploadedEmails.map((email, index) => (
                        <li key={index} className="p-2 border-b">
                            {email.subject} - <span className="text-blue-600">{email.status}</span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
