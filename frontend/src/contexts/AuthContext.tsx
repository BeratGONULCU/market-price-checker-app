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
    const token = localStorage.getItem('token');
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Error fetching user:', error);
      localStorage.removeItem('token'); // Token geçersizse sil
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (token: string) => {
    localStorage.setItem('token', token);
    await fetchUser();
  };

  const logout = () => {
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
      {!loading && children}
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