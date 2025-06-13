import { Product } from './product';

export interface ShoppingList {
  id: number;
  name: string;
  user_id: number;
  created_at: string;
  updated_at: string;
  items: ShoppingListItem[];
}

export interface ShoppingListItem {
  id: number;
  shopping_list_id: number;
  product_id: number;
  quantity: number;
  notes?: string;
  created_at: string;
  updated_at: string;
  product?: Product;
} 