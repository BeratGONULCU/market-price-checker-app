export interface Product {
  id: number;
  name: string;
  description?: string;
  brand?: string;
  image_url?: string;
  barcode?: string;
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
  product: Product;
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
  password: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  is_superuser: boolean;
}

export interface Category {
  id: number;
  name: string;
  description?: string;
  parent_id?: number;
  created_at: string;
  updated_at: string;
}

export interface ShoppingList {
  id: number;
  user_id: number;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface ShoppingListItem {
  id: number;
  shopping_list_id: number;
  product_id: number;
  quantity: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

// Extended interfaces for frontend use
export interface ShoppingListWithItems extends ShoppingList {
  items: ShoppingListItemWithProduct[];
}

export interface ShoppingListItemWithProduct extends ShoppingListItem {
  product: Product;
}

export interface CategoryWithProducts extends Category {
  products: Product[];
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

// Form types
export interface CreateShoppingListForm {
  name: string;
}

export interface AddItemToListForm {
  product_id: number;
  quantity: number;
  notes?: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}
