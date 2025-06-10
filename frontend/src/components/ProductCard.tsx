import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardMedia, Typography, Button, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, Select, MenuItem, FormControl, InputLabel, Snackbar, Alert } from '@mui/material';
import { Favorite, FavoriteBorder, CompareArrows } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import { Product } from '../types';

interface ProductCardProps {
  product: Product;
  onCompare: (productId: number) => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onCompare }) => {
  console.log('ProductCard rendering for product:', product);
  
  const { isAuthenticated, user } = useAuth();
  const [isFavorite, setIsFavorite] = useState(false);
  const [openMarketDialog, setOpenMarketDialog] = useState(false);
  const [selectedMarketId, setSelectedMarketId] = useState<number | ''>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('Auth status:', { isAuthenticated, user });
    if (isAuthenticated && user) {
      checkFavoriteStatus();
    }
  }, [isAuthenticated, user, product.id]);

  const checkFavoriteStatus = async () => {
    try {
      const response = await axios.get(`/api/v1/favorites/check/${product.id}`);
      console.log('Favorite status:', response.data);
      setIsFavorite(response.data.is_favorite);
    } catch (error) {
      console.error('Error checking favorite status:', error);
      setError('Favori durumu kontrol edilirken bir hata oluştu');
    }
  };

  const toggleFavorite = async () => {
    if (!isAuthenticated || !user) {
      console.log('User not authenticated');
      setError('Favori eklemek için giriş yapmalısınız');
      return;
    }

    setIsLoading(true);
    try {
      if (isFavorite) {
        console.log('Removing favorite for product:', product.id);
        await axios.delete(`/api/v1/favorites/${product.id}`);
        console.log('Favorite removed successfully');
      } else {
        console.log('Adding favorite for product:', product.id);
        // En düşük fiyatlı marketi seç
        const lowestPriceDetail = product.details.reduce((prev, current) => 
          (prev.price < current.price) ? prev : current
        );
        
        console.log('Selected market:', lowestPriceDetail.market);
        
        const response = await axios.post(`/api/v1/favorites/${product.id}`, {
          market_id: lowestPriceDetail.market_id
        });
        console.log('Favorite added successfully:', response.data);
      }
      setIsFavorite(!isFavorite);
    } catch (error: any) {
      console.error('Error toggling favorite:', error.response?.data || error.message);
      setError(error.response?.data?.detail || 'Favori işlemi sırasında bir hata oluştu');
    } finally {
      setIsLoading(false);
    }
  };

  const handleMarketSelect = async () => {
    if (!selectedMarketId) return;

    try {
      await axios.post('/api/favorites', {
        product_id: product.id,
        market_id: selectedMarketId
      });
      setIsFavorite(true);
      setOpenMarketDialog(false);
    } catch (error) {
      console.error('Favori eklenirken hata:', error);
    }
  };

  const removeFavorite = async () => {
    try {
      // Favori ID'sini bul ve sil
      const response = await axios.get('/api/favorites');
      const favorite = response.data.find(
        (f: any) => f.product_id === product.id && f.market_id === selectedMarketId
      );
      
      if (favorite) {
        await axios.delete(`/api/favorites/${favorite.id}`);
        setIsFavorite(false);
      }
    } catch (error) {
      console.error('Favori silinirken hata:', error);
    }
  };

  const lowestPrice = Math.min(...product.details.map(detail => detail.price));
  const lowestPriceMarket = product.details.find(detail => detail.price === lowestPrice)?.market.name;

  const handleFavoriteClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    console.log('Favorite button clicked for product:', product.id);
    toggleFavorite();
  };

  return (
    <>
      <Card sx={{ maxWidth: 345, m: 2 }}>
        <CardMedia
          component="img"
          height="140"
          image={product.image_url || '/placeholder.png'}
          alt={product.name}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {product.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {product.description}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Brand: {product.brand}
          </Typography>
          <Typography variant="h6" color="primary">
            Lowest Price: ${lowestPrice.toFixed(2)} at {lowestPriceMarket}
          </Typography>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem' }}>
            <IconButton
              onClick={handleFavoriteClick}
              disabled={isLoading}
              color={isFavorite ? "error" : "default"}
              size="large"
            >
              {isFavorite ? <Favorite /> : <FavoriteBorder />}
            </IconButton>
            <Button
              variant="contained"
              startIcon={<CompareArrows />}
              onClick={() => onCompare(product.id)}
            >
              Karşılaştır
            </Button>
          </div>
        </CardContent>
      </Card>

      <Dialog open={openMarketDialog} onClose={() => setOpenMarketDialog(false)}>
        <DialogTitle>Market Seçin</DialogTitle>
        <DialogContent>
          <FormControl fullWidth>
            <InputLabel>Market</InputLabel>
            <Select
              value={selectedMarketId}
              onChange={(e) => setSelectedMarketId(e.target.value as number)}
            >
              {product.details.map((detail) => (
                <MenuItem key={detail.market_id} value={detail.market_id}>
                  {detail.market.name} - {detail.price} TL
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenMarketDialog(false)}>İptal</Button>
          <Button onClick={handleMarketSelect} variant="contained" color="primary">
            Favorilere Ekle
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError(null)}
      >
        <Alert onClose={() => setError(null)} severity="error">
          {error}
        </Alert>
      </Snackbar>
    </>
  );
};

export default ProductCard; 