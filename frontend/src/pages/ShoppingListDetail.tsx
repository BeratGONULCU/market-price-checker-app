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
  Checkbox
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { useSnackbar } from 'notistack';
import { ShoppingList, Product } from '../types';
import shoppingListService from '../services/shoppingList';

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
    }
  }, [id]);

  const fetchList = async () => {
    try {
      setLoading(true);
      const data = await shoppingListService.getList(Number(id));
      setList(data);
    } catch (error) {
      console.error('Error fetching shopping list:', error);
      enqueueSnackbar('Alışveriş listesi yüklenirken bir hata oluştu', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleAddItem = async () => {
    if (!newItem.product_id || newItem.quantity < 1) {
      enqueueSnackbar('Lütfen geçerli bir ürün ve miktar seçin', { variant: 'error' });
      return;
    }

    try {
      const updatedList = await shoppingListService.addItem(Number(id), newItem.product_id, newItem.quantity);
      setList(updatedList);
      setNewItem({ product_id: 0, quantity: 1 });
      setOpenDialog(false);
      enqueueSnackbar('Ürün listeye eklendi', { variant: 'success' });
    } catch (error) {
      console.error('Error adding item to list:', error);
      enqueueSnackbar('Ürün listeye eklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    try {
      await shoppingListService.removeItem(itemId);
      setList(prev => {
        if (!prev) return null;
        return {
          ...prev,
          items: prev.items.filter(item => item.id !== itemId)
        };
      });
      enqueueSnackbar('Ürün listeden kaldırıldı', { variant: 'success' });
    } catch (error) {
      console.error('Error removing item from list:', error);
      enqueueSnackbar('Ürün listeden kaldırılırken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleToggleItem = async (itemId: number, completed: boolean) => {
    try {
      await shoppingListService.updateItem(itemId, { completed });
      setList(prev => {
        if (!prev) return null;
        return {
          ...prev,
          items: prev.items.map(item =>
            item.id === itemId ? { ...item, completed } : item
          )
        };
      });
    } catch (error) {
      console.error('Error updating item status:', error);
      enqueueSnackbar('Ürün durumu güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!list) {
    return (
      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h6" color="error">
          Liste bulunamadı
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          {list.name}
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Ürün Ekle
        </Button>
      </Box>

      {list.items.length === 0 ? (
        <Typography variant="body1" color="text.secondary">
          Bu listede henüz ürün bulunmamaktadır.
        </Typography>
      ) : (
        <List>
          {list.items.map((item, index) => (
            <React.Fragment key={item.id}>
              <ListItem>
                <Checkbox
                  checked={item.completed}
                  onChange={(e) => handleToggleItem(item.id, e.target.checked)}
                />
                <ListItemText
                  primary={item.product.name}
                  secondary={`Miktar: ${item.quantity}`}
                  sx={{
                    textDecoration: item.completed ? 'line-through' : 'none',
                    color: item.completed ? 'text.secondary' : 'text.primary'
                  }}
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

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Ürün Ekle</DialogTitle>
        <DialogContent>
          <TextField
            select
            fullWidth
            label="Ürün"
            value={newItem.product_id}
            onChange={(e) => setNewItem(prev => ({ ...prev, product_id: Number(e.target.value) }))}
            sx={{ mt: 2 }}
          >
            {products.map((product) => (
              <option key={product.id} value={product.id}>
                {product.name}
              </option>
            ))}
          </TextField>
          <TextField
            fullWidth
            type="number"
            label="Miktar"
            value={newItem.quantity}
            onChange={(e) => setNewItem(prev => ({ ...prev, quantity: Number(e.target.value) }))}
            sx={{ mt: 2 }}
            inputProps={{ min: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>İptal</Button>
          <Button onClick={handleAddItem} color="primary">
            Ekle
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ShoppingListDetail; 