import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  TextField,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Divider,
  Paper
} from '@mui/material';
import { Add as AddIcon, Remove as RemoveIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { Product } from '../types';
import cartService from '../services/cart';
import { useSnackbar } from 'notistack';

interface CartItem {
  id: number;
  product: Product;
  quantity: number;
}

const Cart: React.FC = () => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [quantities, setQuantities] = useState<{ [key: number]: number }>({});
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      setLoading(true);
      const data = await cartService.getCart();
      setCartItems(data);
      // Her ürün için başlangıç miktarını 1 olarak ayarla
      const initialQuantities = data.reduce((acc: { [key: number]: number }, item: CartItem) => {
        acc[item.id] = item.quantity;
        return acc;
      }, {});
      setQuantities(initialQuantities);
    } catch (error) {
      console.error('Error fetching cart:', error);
      enqueueSnackbar('Sepet yüklenirken bir hata oluştu', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleQuantityChange = async (itemId: number, newQuantity: number) => {
    if (newQuantity < 1) return;

    try {
      await cartService.updateQuantity(itemId, newQuantity);
      setQuantities(prev => ({ ...prev, [itemId]: newQuantity }));
      enqueueSnackbar('Ürün miktarı güncellendi', { variant: 'success' });
    } catch (error) {
      console.error('Error updating quantity:', error);
      enqueueSnackbar('Ürün miktarı güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    try {
      await cartService.removeFromCart(itemId);
      setCartItems(prev => prev.filter(item => item.id !== itemId));
      enqueueSnackbar('Ürün sepetten kaldırıldı', { variant: 'success' });
    } catch (error) {
      console.error('Error removing item:', error);
      enqueueSnackbar('Ürün sepetten kaldırılırken bir hata oluştu', { variant: 'error' });
    }
  };

  const calculateTotal = () => {
    return cartItems.reduce((total, item) => {
      const quantity = quantities[item.id] || 1;
      const lowestPrice = Math.min(...item.product.details.map(detail => detail.price));
      return total + (lowestPrice * quantity);
    }, 0);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Sepetim
      </Typography>

      {cartItems.length === 0 ? (
        <Typography variant="body1" color="text.secondary">
          Sepetinizde ürün bulunmamaktadır.
        </Typography>
      ) : (
        <>
          <List>
            {cartItems.map((item, index) => (
              <React.Fragment key={item.id}>
                <ListItem>
                  <ListItemText
                    primary={item.product.name}
                    secondary={`En düşük fiyat: ${Math.min(...item.product.details.map(detail => detail.price))} TL`}
                  />
                  <Box display="flex" alignItems="center" mr={2}>
                    <IconButton
                      size="small"
                      onClick={() => handleQuantityChange(item.id, (quantities[item.id] || 1) - 1)}
                    >
                      <RemoveIcon />
                    </IconButton>
                    <TextField
                      size="small"
                      type="number"
                      value={quantities[item.id] || 1}
                      onChange={(e) => handleQuantityChange(item.id, parseInt(e.target.value))}
                      inputProps={{ min: 1, style: { textAlign: 'center' } }}
                      sx={{ width: '60px', mx: 1 }}
                    />
                    <IconButton
                      size="small"
                      onClick={() => handleQuantityChange(item.id, (quantities[item.id] || 1) + 1)}
                    >
                      <AddIcon />
                    </IconButton>
                  </Box>
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
                {index < cartItems.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>

          <Paper sx={{ p: 2, mt: 2 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="h6">
                Toplam: {calculateTotal().toFixed(2)} TL
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate('/checkout')}
              >
                Siparişi Tamamla
              </Button>
            </Box>
          </Paper>
        </>
      )}
    </Container>
  );
};

export default Cart; 