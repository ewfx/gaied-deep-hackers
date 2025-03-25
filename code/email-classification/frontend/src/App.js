import React from "react";
import UploadForm from "./UploadForm";
import "./styles.css";

function App() {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold text-center">Email Classification</h1>
      <UploadForm />
    </div>
  );
}

export default App;
