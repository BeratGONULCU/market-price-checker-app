import { ShoppingListType as ShoppingList } from '../types/index';
import api from './api';

const shoppingListService = {
  getLists: async (): Promise<ShoppingList[]> => {
    const response = await api.get('/api/v1/shopping-lists/');
    return response.data;
  },

  getList: async (id: number): Promise<ShoppingList> => {
    const response = await api.get(`/api/v1/shopping-lists/${id}/`);
    return response.data;
  },

  createList: async (name: string): Promise<ShoppingList> => {
    const response = await api.post('/api/v1/shopping-lists/', {
      name: name,
      items: []
    });
    return response.data;
  },

  updateList: async (id: number, name: string): Promise<ShoppingList> => {
    const response = await api.put(`/api/v1/shopping-lists/${id}/`, { name });
    return response.data;
  },

  deleteList: async (id: number): Promise<void> => {
    await api.delete(`/api/v1/shopping-lists/${id}/`);
  },

  addItem: async (listId: number, productId: number, quantity: number): Promise<ShoppingList> => {
    const response = await api.post(`/api/v1/shopping-lists/${listId}/items/`, {
      product_id: productId,
      quantity
    });
    return response.data;
  },

  updateItem: async (itemId: number, data: { completed?: boolean; quantity?: number }): Promise<ShoppingList> => {
    const response = await api.put(`/api/v1/shopping-list-items/${itemId}/`, data);
    return response.data;
  },

  removeItem: async (itemId: number): Promise<void> => {
    await api.delete(`/api/v1/shopping-list-items/${itemId}/`);
  }
};

export default shoppingListService; 