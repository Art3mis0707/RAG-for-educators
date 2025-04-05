// /client/src/components/UploadDoc.js
import React, { useState } from 'react';
import './UploadDoc.css';

function UploadDoc() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [message, setMessage] = useState("");
  const [showModal, setShowModal] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    console.log("Selected file:", selectedFile);
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }
    
    const formData = new FormData();
    formData.append("docfile", file);
    
    try {
      const response = await fetch("http://localhost:5004/api/upload-document", {
        method: "POST",
        body: formData
      });
      const data = await response.json();
      if (response.ok) {
        setResult(data.result);
        setMessage("File processed successfully!");
        setShowModal(true);
      } else {
        setMessage(data.message || "Error processing file.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      setMessage("Error uploading file.");
    }
  };

  const handleBoxClick = () => {
    document.getElementById('fileInput').click();
  };

  const closeModal = () => {
    setShowModal(false);
  };

  return (
    <div className="upload-container">
      <div className="upload-box" onClick={handleBoxClick}>
        <div className="upload-icon">📤</div>
        <p className="upload-instructions">
          Drag & drop your .docx file here, or click to select a file.
        </p>
        <input 
          id="fileInput"
          type="file" 
          accept=".docx" 
          onChange={handleFileChange} 
          className="file-input"
        />
      </div>
      <button onClick={handleUpload} className="upload-button">Upload and Process</button>
      {message && <p className="upload-message">{message}</p>}
      
      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button className="close-button" onClick={closeModal}>X</button>
            <h3>Extracted Data</h3>
            <pre>{result}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default UploadDoc;
