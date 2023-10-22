import axios from 'axios';

const API_BASE_URL = 'http://51.20.187.212'; // Update with your API URL

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const registerUser = (userData) => api.post('/api/register/', userData);
export const loginUser = (userData) => api.post('/api/login/', userData);
export const logoutUser = () => api.post('/api/logout/');
export const uploadFile = (file) => api.post('/api/upload/', file, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });


export const setAuthToken = (token) => {
  api.defaults.headers.common['Authorization'] = `Token ${token}`;
};

export const clearAuthToken = () => {
  delete api.defaults.headers.common['Authorization'];
};

export default api;
