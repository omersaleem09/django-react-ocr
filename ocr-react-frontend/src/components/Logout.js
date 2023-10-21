import React from 'react';
import { logoutUser, clearAuthToken } from '../services/api';
import { useNavigate } from "react-router-dom";

function Logout() {
  const navigate = useNavigate();
  const handleLogout = async () => {
    try {
      await logoutUser();
      clearAuthToken();
      alert('Logout successful!');
    } catch (error) {
      alert('Logout failed.');
    }
  };

  return (
    <div>
      <h2>Logged out successfully</h2>
      <button onClick={handleLogout} style={{ display: 'none' }}>Logout</button>
      <button onClick={() => navigate('/login')}>Login</button>
    </div>
  );
}

export default Logout;
