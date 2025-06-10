export interface Market {
  id: number;
  name: string;
  logo_url?: string;
  website?: string;
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
} 