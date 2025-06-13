import React, { createContext, useContext, useState, useEffect } from 'react';
import authService from '../services/auth';

interface User {
  id: number;
  email: string;
  name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string | null;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (token: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      console.log('AuthProvider - Initializing auth...');
      const token = localStorage.getItem('token');
      console.log('AuthProvider - Token exists:', !!token);

      if (token) {
        try {
          console.log('AuthProvider - Fetching user data...');
          const userData = await authService.getCurrentUser();
          console.log('AuthProvider - User data:', userData);
          setUser(userData);
        } catch (error) {
          console.error('AuthProvider - Error fetching user:', error);
          localStorage.removeItem('token');
          setUser(null);
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (token: string) => {
    console.log('AuthProvider - Logging in...');
    localStorage.setItem('token', token);
    try {
      const userData = await authService.getCurrentUser();
      console.log('AuthProvider - Login successful, user data:', userData);
      setUser(userData);
    } catch (error) {
      console.error('AuthProvider - Error during login:', error);
      localStorage.removeItem('token');
      setUser(null);
      throw error;
    }
  };

  const logout = () => {
    console.log('AuthProvider - Logging out...');
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 