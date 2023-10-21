import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import Routes instead of Switch
import Register from '../components/Register';
import Login from '../components/Login';
import Logout from '../components/Logout';
import FileUpload from '../components/FileUpload';
import Home from '../components/Home'

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/upload" element={<FileUpload />} /> {/* Add the new route */}
        </Routes>
      </Router>
    </div>
  );
}

export default App;
