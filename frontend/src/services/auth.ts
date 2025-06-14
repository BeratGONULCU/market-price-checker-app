import { User, RegisterRequest } from '../types';
import api from './api';

interface LoginRequest {
  email: string;
  password: string;
}

interface UpdateProfileRequest {
  name?: string;
  email?: string;
  password?: string;
  image_url?: string;
}

const authService = {
  login: async (data: LoginRequest): Promise<{ token: string; user: User }> => {
    const response = await api.post('/api/auth/login/', data);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<{ token: string; user: User }> => {
    const response = await api.post('/api/auth/register/', data);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/api/auth/me/');
    return response.data;
  },

  updateProfile: async (data: UpdateProfileRequest): Promise<User> => {
    const response = await api.put('/api/auth/me/', data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    localStorage.removeItem('token');
  }
};

export default authService; 