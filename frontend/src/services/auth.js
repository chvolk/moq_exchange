import api from './api';

const authService = {
  async login(username, password) {
    try {
      const response = await api.post('/login/', { username, password });
      const token = response.data.token;
      console.log('Received token:', token); // Debug log
      localStorage.setItem('token', token);
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      this.logAxiosError(error);
      throw error;
    }
  },
  signup(user) {
    return api.post('/signup/', user);
  },
  logAxiosError(error) {
    if (error.response) {
      console.error('Error response:', error.response);
      console.error('Error data:', error.response.data);
      console.error('Error status:', error.response.status);
      console.error('Error headers:', error.response.headers);
    } else if (error.request) {
      console.error('Error request:', error.request);
    } else {
      console.error('Error message:', error.message);
    }
  }
};

export default authService;