import api from './api';

export interface Category {
  id: number;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export const categoryService = {
  getAllCategories: async () => {
    const response = await api.get('/categories');
    return response.data;
  },

  getCategoryById: async (id: number) => {
    const response = await api.get(`/categories/${id}`);
    return response.data;
  },
}; 