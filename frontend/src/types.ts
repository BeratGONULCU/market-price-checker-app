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
  name: string;
  email: string;
  image_url?: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  parent_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface ShoppingList {
  id: number;
  name: string;
  user_id: number;
  items: ShoppingListItem[];
  created_at: string;
  updated_at: string;
}

export interface ShoppingListItem {
  id: number;
  shopping_list_id: number;
  product_id: number;
  product: Product;
  quantity: number;
  completed: boolean;
  is_checked: boolean;
  created_at: string;
  updated_at: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}
