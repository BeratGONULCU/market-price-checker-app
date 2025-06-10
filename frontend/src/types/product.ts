export interface Product {
  id: number;
  name: string;
  description: string;
  image_url?: string;
  category_id: number;
  created_at: string;
  updated_at: string;
  details: ProductDetail[];
  is_favorite?: boolean;
}

export interface ProductDetail {
  id: number;
  product_id: number;
  market_id: number;
  price: number;
  calories: number;
  expiration_date: string;
  is_favorite: boolean;
  created_at: string;
  updated_at: string;
  market?: Market;
  product?: Product;
}

export interface Market {
  id: number;
  name: string;
  logo_url?: string;
  website?: string;
} 