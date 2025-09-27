import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { FaFileUpload } from 'react-icons/fa';

const UploadTranscriptPage = () => {
  const { user } = useAuth();
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check if the file is a JSON file
      if (file.type === 'application/json') {
        setSelectedFile(file);
        setError('');
      } else {
        setSelectedFile(null);
        setError('Error: Please upload a valid .json file.');
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedFile) {
      // For this mock-up, we'll just show an alert.
      // In a real app, you would send the 'selectedFile' object to your backend.
      alert(`File "${selectedFile.name}" uploaded successfully!`);
      setSelectedFile(null);
      setError('');
    }
  };

  return (
    <>
      <header className="app-header">
        <h2 className="page-subtitle">Upload Meeting Transcript</h2>
      </header>
      <div className="upload-container">
        <form onSubmit={handleSubmit}>
          <p>Select a JSON transcript file from a past meeting to upload.</p>
          
          {/* Hidden file input */}
          <input 
            type="file"
            id="file-upload"
            onChange={handleFileChange}
            accept=".json"
            style={{ display: 'none' }}
          />
          
          {/* Custom styled button */}
          <label htmlFor="file-upload" className="button-secondary upload-label">
            <FaFileUpload />
            Choose File
          </label>
          
          {/* Display selected file info or error */}
          <div className="file-info">
            {selectedFile && <p>Selected: <strong>{selectedFile.name}</strong></p>}
            {error && <p className="error-message">{error}</p>}
          </div>
          
          <button 
            type="submit" 
            className="button-primary" 
            disabled={!selectedFile}
          >
            Upload
          </button>
        </form>
      </div>
    </>
  );
};

export default UploadTranscriptPage;