import api from './api';
import { ProductDetail } from '../types';

const favoriteService = {
  async getFavorites(): Promise<ProductDetail[]> {
    const response = await api.get('/api/v1/favorites');
    return response.data;
  },

  async addFavorite(productId: number, marketId: number): Promise<ProductDetail> {
    const response = await api.patch(`/api/v1/products/${productId}/details/${marketId}/favorite`);
    return response.data;
  },

  async removeFavorite(productId: number, marketId: number): Promise<ProductDetail> {
    const response = await api.patch(`/api/v1/products/${productId}/details/${marketId}/favorite`);
    return response.data;
  },

  async isFavorite(productId: number, marketId: number): Promise<boolean> {
    try {
      const response = await api.get(`/api/v1/products/${productId}/details/${marketId}`);
      return response.data.is_favorite;
    } catch (error) {
      return false;
    }
  }
};

export default favoriteService; 