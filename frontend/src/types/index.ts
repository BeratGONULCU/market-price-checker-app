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

export interface Price {
  market_id: number;
  market_name: string;
  price: number;
}

export interface ProductDetail {
  id: number;
  product_id: number;
  market_id: number;
  price: number;
  expiration_date: string;
  calories: number;
  is_favorite: boolean;
  created_at: string;
  updated_at: string;
  market: Market;
}

export interface Product {
  id: number;
  name: string;
  description?: string;
  brand?: string;
  barcode?: string;
  image_url?: string;
  category_id: number;
  category: Category;
  details: ProductDetail[];
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  description?: string;
  parent_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface PriceAlert {
  id: number;
  product_id: number;
  user_id: number;
  target_price: number;
  created_at: string;
  updated_at: string;
}

export interface Favorite {
  id: number;
  product_id: number;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  email: string;
  name: string;
  image_url?: string;
  created_at: string;
  updated_at: string;
}

export interface ShoppingListItem {
  id: number;
  shopping_list_id: number;
  product_id: number;
  quantity: number;
  is_checked: boolean;
  notes?: string;
  product: Product;
  created_at: string;
  updated_at: string;
}

export interface ShoppingList {
  id: number;
  user_id: number;
  name: string;
  items: ShoppingListItem[];
  created_at: string;
  updated_at: string;
}

export interface Store {
  id: number;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  created_at: string;
  updated_at: string;
}

export interface Price {
  id: number;
  product_id: number;
  store_id: number;
  price: number;
  created_at: string;
  updated_at: string;
  product?: Product;
  store?: Store;
}

export type { ShoppingList as ShoppingListType };
export type { ShoppingListItem as ShoppingListItemType };

