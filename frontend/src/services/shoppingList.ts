import api from './api';
import { ShoppingList, ShoppingListItem } from '../types/shoppingList';

const shoppingListService = {
  // Alışveriş listelerini getir
  async getShoppingLists(): Promise<ShoppingList[]> {
    const response = await api.get<ShoppingList[]>('/api/v1/shopping-lists');
    return response.data;
  },

  // Tek bir alışveriş listesini getir
  async getShoppingList(id: number): Promise<ShoppingList> {
    const response = await api.get<ShoppingList>(`/api/v1/shopping-lists/${id}`);
    return response.data;
  },

  // Yeni alışveriş listesi oluştur
  async createShoppingList(name: string): Promise<ShoppingList> {
    const response = await api.post<ShoppingList>('/api/v1/shopping-lists', { name });
    return response.data;
  },

  // Alışveriş listesini güncelle
  async updateShoppingList(id: number, name: string): Promise<ShoppingList> {
    const response = await api.put<ShoppingList>(`/api/v1/shopping-lists/${id}`, { name });
    return response.data;
  },

  // Alışveriş listesini sil
  async deleteShoppingList(id: number): Promise<void> {
    await api.delete(`/api/v1/shopping-lists/${id}`);
  },

  // Listeye ürün ekle
  async addItemToList(listId: number, productId: number, quantity: number, notes?: string): Promise<ShoppingListItem> {
    const response = await api.post<ShoppingListItem>(`/api/v1/shopping-lists/${listId}/items`, {
      product_id: productId,
      quantity,
      notes
    });
    return response.data;
  },

  // Liste öğesini güncelle
  async updateListItem(itemId: number, quantity: number, notes?: string): Promise<ShoppingListItem> {
    const response = await api.put<ShoppingListItem>(`/api/v1/shopping-lists/items/${itemId}`, {
      quantity,
      notes
    });
    return response.data;
  },

  // Liste öğesini sil
  async deleteListItem(itemId: number): Promise<void> {
    await api.delete(`/api/v1/shopping-lists/items/${itemId}`);
  }
};

export default shoppingListService; 