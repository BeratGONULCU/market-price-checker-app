import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  IconButton,
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  Snackbar
} from '@mui/material';
import {
  Favorite as FavoriteIcon,
  FavoriteBorder as FavoriteBorderIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { Product, ProductDetail } from '../types/product';
import { Market } from '../types/market';
import { ShoppingList } from '../types/shoppingList';
import axios from 'axios';

const MarketDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [market, setMarket] = useState<Market | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [selectedList, setSelectedList] = useState<number | null>(null);
  const [shoppingLists, setShoppingLists] = useState<ShoppingList[]>([]);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error'
  });

  useEffect(() => {
    const fetchMarketDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/v1/markets/${id}`);
        setMarket(response.data);
      } catch (err) {
        setError('Market detayları yüklenirken bir hata oluştu');
        console.error('Error fetching market details:', err);
      }
    };

    const fetchProducts = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/v1/markets/${id}/products`);
        setProducts(response.data);
      } catch (err) {
        setError('Ürünler yüklenirken bir hata oluştu');
        console.error('Error fetching products:', err);
      }
    };

    const fetchFavorites = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/favorites', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        setFavorites(response.data.map((fav: any) => fav.product_id));
      } catch (err) {
        console.error('Error fetching favorites:', err);
      }
    };

    const fetchShoppingLists = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/shopping-lists', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        setShoppingLists(response.data);
        if (response.data.length > 0) {
          setSelectedList(response.data[0].id);
        }
      } catch (err) {
        console.error('Error fetching shopping lists:', err);
      }
    };

    const loadData = async () => {
      setLoading(true);
      await Promise.all([
        fetchMarketDetails(),
        fetchProducts(),
        fetchFavorites(),
        fetchShoppingLists()
      ]);
      setLoading(false);
    };

    loadData();
  }, [id]);

  const handleToggleFavorite = async (productId: number) => {
    try {
      const isFavorite = favorites.includes(productId);
      const method = isFavorite ? 'DELETE' : 'POST';
      await axios({
        method,
        url: `http://localhost:8000/api/v1/favorites/${productId}`,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      setFavorites(prev =>
        isFavorite
          ? prev.filter(id => id !== productId)
          : [...prev, productId]
      );

      setSnackbar({
        open: true,
        message: isFavorite ? 'Ürün favorilerden çıkarıldı' : 'Ürün favorilere eklendi',
        severity: 'success'
      });
    } catch (err) {
      console.error('Error toggling favorite:', err);
      setSnackbar({
        open: true,
        message: 'Favori işlemi sırasında bir hata oluştu',
        severity: 'error'
      });
    }
  };

  const handleAddToList = async (productId: number) => {
    if (!selectedList) return;

    try {
      await axios.post(`http://localhost:8000/api/v1/shopping-lists/${selectedList}/items`, {
        product_id: productId,
        quantity: quantity
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      setSnackbar({
        open: true,
        message: 'Ürün alışveriş listesine eklendi',
        severity: 'success'
      });
      setOpenDialog(false);
    } catch (err) {
      console.error('Error adding to list:', err);
      setSnackbar({
        open: true,
        message: 'Ürün listeye eklenirken bir hata oluştu',
        severity: 'error'
      });
    }
  };

  if (loading) return <Typography>Yükleniyor...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!market) return <Typography>Market bulunamadı</Typography>;

    return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Market Bilgileri */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          {market.name}
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          {market.description}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Adres: {market.address}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Telefon: {market.phone}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Çalışma Saatleri: {market.open_hours}
        </Typography>
      </Box>

      {/* Ürünler */}
      <Typography variant="h5" gutterBottom>
        Ürünler
          </Typography>
        <Grid container spacing={3}>
        {products.map((product) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={product.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative',
                '&:hover': {
                  boxShadow: 6,
                  cursor: 'pointer'
                }
              }}
              onClick={() => navigate(`/products/${product.id}`)}
            >
              <CardMedia
                component="img"
                height="200"
                image={product.image_url || '/placeholder.png'}
                alt={product.name}
                sx={{
                  objectFit: 'contain',
                  bgcolor: 'grey.100',
                  p: 2
                }}
              />
              <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                <Typography
                  gutterBottom
                  variant="h6"
                  component="div"
                  sx={{
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    height: '3.6em',
                    lineHeight: '1.2em'
                }}
              >
                  {product.name}
                </Typography>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    height: '2.4em',
                    lineHeight: '1.2em',
                    mb: 1
                  }}
                >
                  {product.description}
                </Typography>
                <Box sx={{ mt: 'auto' }}>
                  <Typography variant="h6" color="primary" gutterBottom>
                    {product.details[0]?.price.toLocaleString('tr-TR', {
                      style: 'currency',
                      currency: 'TRY'
                    })}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {product.details[0]?.unit}
                  </Typography>
                </Box>
              </CardContent>
              <Box sx={{ position: 'absolute', top: 8, right: 8, display: 'flex', gap: 1 }}>
                <IconButton
                  sx={{
                    bgcolor: 'background.paper',
                    '&:hover': {
                      bgcolor: 'action.hover'
                    }
                  }}
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedProduct(product);
                    setOpenDialog(true);
                  }}
                >
                  <AddIcon />
                </IconButton>
                <IconButton
                  sx={{
                    bgcolor: 'background.paper',
                    '&:hover': {
                      bgcolor: 'action.hover'
                    }
                  }}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleToggleFavorite(product.id);
                  }}
                >
                  {favorites.includes(product.id) ? (
                    <FavoriteIcon color="error" />
                  ) : (
                    <FavoriteBorderIcon />
                  )}
                </IconButton>
              </Box>
            </Card>
          </Grid>
        ))}
          </Grid>

      {/* Alışveriş Listesine Ekleme Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Alışveriş Listesine Ekle</DialogTitle>
        <DialogContent>
          <TextField
            select
            fullWidth
            label="Alışveriş Listesi"
            value={selectedList || ''}
            onChange={(e) => setSelectedList(Number(e.target.value))}
            margin="normal"
            SelectProps={{
              native: true
            }}
          >
            {shoppingLists.map((list) => (
              <option key={list.id} value={list.id}>
                {list.name}
              </option>
            ))}
          </TextField>
          <TextField
            fullWidth
            label="Miktar"
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(Number(e.target.value))}
            margin="normal"
            inputProps={{ min: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>İptal</Button>
          <Button 
            onClick={() => selectedProduct && handleAddToList(selectedProduct.id)} 
            variant="contained" 
            color="primary"
          >
            Ekle
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
      </Container>
  );
};

export default MarketDetail; 