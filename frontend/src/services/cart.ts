import { Product } from '../types';
import api from './api';

interface CartItem {
  id: number;
  product: Product;
  quantity: number;
}

const cartService = {
  getCart: async (): Promise<CartItem[]> => {
    const response = await api.get('/cart/');
    return response.data;
  },

  addToCart: async (productId: number, quantity: number): Promise<CartItem> => {
    const response = await api.post('/cart/', { product_id: productId, quantity });
    return response.data;
  },

  updateQuantity: async (itemId: number, quantity: number): Promise<CartItem> => {
    const response = await api.put(`/cart/${itemId}/`, { quantity });
    return response.data;
  },

  removeFromCart: async (itemId: number): Promise<void> => {
    await api.delete(`/cart/${itemId}/`);
  }
};

export default cartService; 