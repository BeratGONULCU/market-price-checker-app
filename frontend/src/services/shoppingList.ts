import { ShoppingList } from '../types';
import api from './api';

const shoppingListService = {
  getLists: async (): Promise<ShoppingList[]> => {
    const response = await api.get('/shopping-lists/');
    return response.data;
  },

  getList: async (id: number): Promise<ShoppingList> => {
    const response = await api.get(`/shopping-lists/${id}/`);
    return response.data;
  },

  createList: async (name: string): Promise<ShoppingList> => {
    const response = await api.post('/shopping-lists/', { name });
    return response.data;
  },

  updateList: async (id: number, name: string): Promise<ShoppingList> => {
    const response = await api.put(`/shopping-lists/${id}/`, { name });
    return response.data;
  },

  deleteList: async (id: number): Promise<void> => {
    await api.delete(`/shopping-lists/${id}/`);
  },

  addItem: async (listId: number, productId: number, quantity: number): Promise<ShoppingList> => {
    const response = await api.post(`/shopping-lists/${listId}/items/`, {
      product_id: productId,
      quantity
    });
    return response.data;
  },

  updateItem: async (itemId: number, data: { completed?: boolean; quantity?: number }): Promise<ShoppingList> => {
    const response = await api.put(`/shopping-list-items/${itemId}/`, data);
    return response.data;
  },

  removeItem: async (itemId: number): Promise<void> => {
    await api.delete(`/shopping-list-items/${itemId}/`);
  }
};

export default shoppingListService; 