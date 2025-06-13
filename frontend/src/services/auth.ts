import api from './api';

interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
}

interface UserResponse {
  id: number;
  email: string;
  name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string | null;
}

const authService = {
  async login(data: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await api.post<AuthResponse>('/api/v1/auth/login', data);
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  async register(data: RegisterRequest): Promise<UserResponse> {
    try {
      const response = await api.post<UserResponse>('/api/v1/auth/register', data);
      return response.data;
    } catch (error) {
      console.error('Register error:', error);
      throw error;
    }
  },

  async getCurrentUser(): Promise<UserResponse> {
    try {
      const response = await api.get<UserResponse>('/api/v1/auth/me');
      return response.data;
    } catch (error) {
      console.error('Get current user error:', error);
      throw error;
    }
  },

  async updateProfile(data: Partial<RegisterRequest>): Promise<UserResponse> {
    try {
      const response = await api.put<UserResponse>('/api/v1/auth/me', data);
      return response.data;
    } catch (error) {
      console.error('Update profile error:', error);
      throw error;
    }
  },

  logout() {
    localStorage.removeItem('token');
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  },
};

export default authService; 