export interface Product {
  id: number;
  name: string;
  description: string;
  image_url: string;
  brand: string;
  barcode: string;
  created_at: string;
  updated_at: string;
  details: ProductDetail[];
  category: Category;
}

export interface ProductDetail {
  id: number;
  product_id: number;
  market_id: number;
  price: number;
  expiration_date: string;
  calories: number;
  is_favorite: boolean;  // Favori durumu
  created_at: string;
  updated_at: string;
  market: Market;
}

export interface Market {
  id: number;
  name: string;
  address: string;
  phone: string;
  open_hours: string;
  website: string;
  latitude: number;
  longitude: number;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  email: string;
  name: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  parent_id: number | null;
  created_at: string;
  updated_at: string;
}
