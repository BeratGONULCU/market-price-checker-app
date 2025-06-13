import api from './api';
import { Market } from '../types/market';

export interface Product {
  id: number;
  name: string;
  description: string;
  brand: string | null;
  barcode: string;
  image_url: string | null;
  created_at: string;
  updated_at: string;
  details: ProductDetail[];
  categories: Category[];
}

export interface ProductDetail {
    id: number;
    product_id: number;
    market_id: number;
    price: number;
    unit: string;
    expiration_date: string | null;
    calories: number | null;
    created_at: string;
    updated_at: string;
    is_favorite: boolean;
    market: Market;
}

export interface ProductPrice {
  id: number;
  product_id: number;
  market_id: number;
  price: number;
  expiration_date: string | null;
  calories: number | null;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  parent_id: number | null;
  created_at: string;
  updated_at: string;
}

export const productService = {
  async getAllProducts(): Promise<Product[]> {
    const response = await api.get('/products/');
    return response.data;
  },

  async getProductById(id: number): Promise<Product> {
    const response = await api.get(`/products/${id}/`);
    return response.data;
  },

  async searchProducts(query: string): Promise<Product[]> {
    const response = await api.get(`/products/search/`, {
      params: {
        q: query
      }
    });
    return response.data;
  },

  async getProductsByCategory(categoryId: number): Promise<Product[]> {
    const response = await api.get(`/products/category/${categoryId}/`);
    return response.data;
  },

  async getProductsByMarket(marketId: number): Promise<Product[]> {
    const response = await api.get(`/products/market/${marketId}/`);
    return response.data;
  },

  async getProductDetails(productId: number): Promise<ProductDetail[]> {
    const response = await api.get(`/products/${productId}/details/`);
    return response.data;
  },

  async getSimilarProducts(productId: number): Promise<Product[]> {
    const response = await api.get(`/products/${productId}/similar`);
    return response.data;
  }
}; 