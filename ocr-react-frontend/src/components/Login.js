import React, { useState } from 'react';
import { loginUser, setAuthToken } from '../services/api';
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await loginUser(formData);
      setAuthToken(response.data.token);
      navigate("/upload")
      alert('Login successful!');
    } catch (error) {
      console.log(error);
      alert('Login failed.');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username or Email"
          name="username"
          onChange={(e) => setFormData({ ...formData, username: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          name="password"
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
