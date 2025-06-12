export interface Product {
  id: number;
  name: string;
  description: string;
  brand: string;
  barcode: string;
  image_url: string;
  created_at: string;
  updated_at: string;
  details: ProductDetail[];
  category: Category;
  is_favorite?: boolean;
}

export interface ProductDetail {
  id: number;
  product_id: number;
  market_id: number;
  price: number;
  unit: string;
  expiration_date: string;
  calories: number;
  is_favorite: boolean;
  created_at: string;
  updated_at: string;
  market: Market;
}

export interface Market {
  id: number;
  name: string;
  logo_url?: string;
  website?: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  parent_id: number | null;
  created_at: string;
  updated_at: string;
} 