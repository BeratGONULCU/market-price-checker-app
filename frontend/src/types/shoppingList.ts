import { Product } from './product';

export interface ShoppingListItem {
  id: number;
  product_id: number;
  quantity: number;
  is_checked: boolean;
  product: Product;
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