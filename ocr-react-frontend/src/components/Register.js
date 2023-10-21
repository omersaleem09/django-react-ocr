import React, { useState } from 'react';
import { registerUser } from '../services/api';
import { useNavigate } from "react-router-dom";


function Register() {
const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });

  const handleSubmit = async (e) => {
    
    e.preventDefault();
    try {
        debugger;
        console.log(formData);
        navigate('/login')
      await registerUser(formData);
      
      alert('Registration successful!');
    } catch (error) {
      alert('Registration failed.');
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          name="username"
          onChange={(e) => setFormData({ ...formData, username: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          name="email"
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          name="password"
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
