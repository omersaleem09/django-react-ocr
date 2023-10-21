import React, { useState } from 'react';
import { uploadFile } from '../services/api';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function FileUpload() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [showModal, setShowModal] = useState(false);

  // Function to handle file input change
  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (file && file.type !== 'application/pdf') {
      // Check if the selected file is not a PDF
      alert('Only PDF files are accepted.');
      e.target.value = null; // Clear the input field
    } else {
      setSelectedFile(file);
    }
  };

  // Function to check if the user is authorized
  const isAuthorized = () => {
    // Implement your authorization logic here, e.g., check user roles or permissions
    // Return true if authorized, false if not
    return true; // Replace with your actual authorization logic
  };

  // Function to handle file upload
  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file to upload.');
      return;
    }

    // Create a FormData object and append the selected file to it
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Show the spinner if authorized
      if (isAuthorized()) {
        setUploading(true);
      }

      // Call the uploadFile function to send the file to the server
      await uploadFile(formData);

      // Hide the spinner
      setUploading(false);

      // Show the success modal
      setShowModal(true);

      // Clear the selected file input
      setSelectedFile(null);
    } catch (error) {
      // Hide the spinner if not authorized
      if (error.request.status === 401) {
        setUploading(false);
        alert("YOU ARE NOT AUTHORIZED TO PERFORM THIS ACTION");
        navigate('/login');
      } else {
        console.log(error.request.status);
        // Handle any errors that occur during the upload
        alert('File upload failed.');
      }
    }
  };

  const closeModal = () => {
    setShowModal(false);
  };

  return (
    <div>
      <button onClick={() => navigate('/logout')}>Logout</button>
      <h2>File Upload</h2>
      {/* Input field for selecting a PDF file */}
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      {/* Button to trigger file upload */}
      <button onClick={handleUpload}>Upload File</button>
      {/* Logout button */}
      

      {/* Conditional rendering of spinner and modal */}
      {uploading && <div className="spinner">Uploading...</div>}
      {showModal && (
        <div className="modal">
          <p>File uploaded successfully!</p>
          <button onClick={closeModal}>Close</button>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
