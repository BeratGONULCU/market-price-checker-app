import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Divider,
  Checkbox,
  MenuItem
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { useSnackbar } from 'notistack';
import axios from 'axios';
import { ShoppingListType as ShoppingList, ShoppingListItemType as ShoppingListItem, Product } from '../types/index';

const ShoppingListDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [list, setList] = useState<ShoppingList | null>(null);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [newItem, setNewItem] = useState({ product_id: 0, quantity: 1 });
  const [products, setProducts] = useState<Product[]>([]);
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (id) {
      fetchList();
      fetchProducts();
    }
  }, [id]);

  const fetchList = async () => {
    try {
      setLoading(true);
      const response = await axios.get<ShoppingList>(`http://localhost:8000/api/v1/shopping-lists/${id}`);
      setList(response.data);
    } catch (error) {
      console.error('Error fetching shopping list:', error);
      enqueueSnackbar('Alışveriş listesi yüklenirken bir hata oluştu', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await axios.get<Product[]>('http://localhost:8000/api/v1/products');
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
      enqueueSnackbar('Ürünler yüklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleAddItem = async () => {
    if (!newItem.product_id || !list) return;

    try {
      const response = await axios.post<ShoppingListItem>(`http://localhost:8000/api/v1/shopping-lists/${id}/items`, {
        product_id: newItem.product_id,
        quantity: newItem.quantity
      });

      const updatedList: ShoppingList = {
        ...list,
        items: [...list.items, response.data]
      };
      setList(updatedList);
      setNewItem({ product_id: 0, quantity: 1 });
      setOpenDialog(false);
      enqueueSnackbar('Ürün listeye eklendi', { variant: 'success' });
    } catch (error) {
      console.error('Error adding item:', error);
      enqueueSnackbar('Ürün eklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    try {
      await axios.delete(`http://localhost:8000/api/v1/shopping-lists/items/${itemId}`);
      if (list) {
        const updatedItems = list.items.filter((item: ShoppingListItem) => item.id !== itemId);
        const updatedList: ShoppingList = {
          ...list,
          items: updatedItems
        };
        setList(updatedList);
        enqueueSnackbar('Ürün listeden kaldırıldı', { variant: 'success' });
      }
    } catch (error) {
      console.error('Error removing item:', error);
      enqueueSnackbar('Ürün kaldırılırken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleToggleItem = async (itemId: number, completed: boolean) => {
    try {
      await axios.put(`http://localhost:8000/api/v1/shopping-lists/items/${itemId}`, {
        is_checked: completed
      });

      if (list) {
        const updatedItems = list.items.map((item: ShoppingListItem) =>
          item.id === itemId ? { ...item, is_checked: completed } : item
        );
        const updatedList: ShoppingList = {
          ...list,
          items: updatedItems
        };
        setList(updatedList);
      }
    } catch (error) {
      console.error('Error updating item:', error);
      enqueueSnackbar('Ürün güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (!list) {
    return (
      <Typography variant="h6" color="error">
        Alışveriş listesi bulunamadı
      </Typography>
    );
  }

  return (
    <Container>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          {list.name}
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
          sx={{ mb: 2 }}
        >
          Ürün Ekle
        </Button>

        {list.items.length === 0 ? (
          <Typography variant="body1" color="text.secondary">
            Bu listede henüz ürün bulunmamaktadır.
          </Typography>
        ) : (
          <List>
            {list.items.map((item: ShoppingListItem, index: number) => (
              <React.Fragment key={item.id}>
                <ListItem>
                  <Checkbox
                    checked={item.is_checked}
                    onChange={(e) => handleToggleItem(item.id, e.target.checked)}
                  />
                  <ListItemText
                    primary={item.product.name}
                    secondary={`${item.quantity} adet`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      aria-label="delete"
                      onClick={() => handleRemoveItem(item.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < list.items.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        )}
      </Box>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Ürün Ekle</DialogTitle>
        <DialogContent>
          <TextField
            select
            fullWidth
            label="Ürün"
            value={newItem.product_id}
            onChange={(e) => setNewItem({ ...newItem, product_id: Number(e.target.value) })}
            sx={{ mt: 2 }}
          >
            {products.map((product) => (
              <MenuItem key={product.id} value={product.id}>
                {product.name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            type="number"
            fullWidth
            label="Adet"
            value={newItem.quantity}
            onChange={(e) => setNewItem({ ...newItem, quantity: Number(e.target.value) })}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>İptal</Button>
          <Button onClick={handleAddItem} variant="contained">
            Ekle
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ShoppingListDetail; 