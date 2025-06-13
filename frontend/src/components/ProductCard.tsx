import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Box,
  Alert,
  CircularProgress
} from '@mui/material';
import { Favorite, FavoriteBorder, Notifications, NotificationsActive } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { Product, Price } from '../types';
import { useNavigate } from 'react-router-dom';
import favoriteService from '../services/favorite';
import priceAlertService from '../services/priceAlert';
import api from '../services/api';

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [isFavorite, setIsFavorite] = useState(false);
  const [isMarketDialogOpen, setIsMarketDialogOpen] = useState(false);
  const [selectedMarketId, setSelectedMarketId] = useState<number | null>(null);
  const [priceAlert, setPriceAlert] = useState<number | null>(null);
  const [showPriceAlertInput, setShowPriceAlertInput] = useState(false);
  const [targetPrice, setTargetPrice] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      checkFavoriteStatus();
      checkPriceAlert();
    }
  }, [user, product.id]);

  const checkFavoriteStatus = async () => {
    try {
      // En düşük fiyatlı marketi seç
      const lowestPriceDetail = product.prices.reduce((prev: Price, current: Price) => 
        (prev.price < current.price) ? prev : current
      );
      const status = await favoriteService.isFavorite(product.id, lowestPriceDetail.market_id);
      setIsFavorite(status);
    } catch (error) {
      console.error('Error checking favorite status:', error);
    }
  };

  const checkPriceAlert = async () => {
    try {
      const alert = await priceAlertService.getProductPriceAlert(product.id);
      if (alert) {
        setPriceAlert(alert.target_price);
      }
    } catch (error) {
      console.error('Error checking price alert:', error);
    }
  };

  const handleToggleFavorite = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      setLoading(true);
      // En düşük fiyatlı marketi seç
      const lowestPriceDetail = product.prices.reduce((prev: Price, current: Price) => 
        (prev.price < current.price) ? prev : current
      );

      console.log('Product prices:', product.prices);
      console.log('Lowest price detail:', lowestPriceDetail);
      console.log('Toggling favorite for product:', product.id, 'market:', lowestPriceDetail.market_id);

      // PATCH isteği gönder
      const response = await api.patch(
        `/api/v1/products/${product.id}/details/${lowestPriceDetail.market_id}/favorite`
      );
      console.log('Favorite toggle response:', response.data);

      setIsFavorite(!isFavorite);
    } catch (error: any) {
      console.error('Favori işlemi sırasında hata:', error);
      if (error.response) {
        console.error('Error response:', error.response.data);
        console.error('Error status:', error.response.status);
      }
      setError('Favori işlemi sırasında bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const handleMarketClick = (marketId: number) => {
    if (!user) {
      navigate('/login');
      return;
    }
    setSelectedMarketId(marketId);
    setIsMarketDialogOpen(true);
  };

  const handlePriceAlertSubmit = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      setLoading(true);
      const targetPriceNum = parseFloat(targetPrice);
      if (isNaN(targetPriceNum) || targetPriceNum <= 0) {
        setError('Lütfen geçerli bir fiyat girin');
        return;
      }

      await priceAlertService.createPriceAlert(product.id, targetPriceNum);
      setPriceAlert(targetPriceNum);
      setShowPriceAlertInput(false);
      setTargetPrice('');
    } catch (error) {
      setError('Fiyat alarmı oluşturulurken bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ maxWidth: 345, height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardMedia
        component="img"
        height="140"
        image={product.image_url || 'https://via.placeholder.com/140'}
        alt={product.name}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography gutterBottom variant="h6" component="div">
          {product.name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {product.description}
        </Typography>
        <Box sx={{ mt: 2 }}>
          {product.prices.map((price: Price) => (
            <Button
              key={price.market_id}
              variant="outlined"
              size="small"
              sx={{ mr: 1, mb: 1 }}
              onClick={() => handleMarketClick(price.market_id)}
            >
              {price.market_name}: {price.price} TL
            </Button>
          ))}
        </Box>
      </CardContent>
      <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <IconButton onClick={handleToggleFavorite} disabled={loading}>
          {isFavorite ? <Favorite color="error" /> : <FavoriteBorder />}
        </IconButton>
        <IconButton
          onClick={() => setShowPriceAlertInput(!showPriceAlertInput)}
          disabled={loading}
        >
          {priceAlert ? <NotificationsActive color="primary" /> : <Notifications />}
        </IconButton>
      </Box>
      {showPriceAlertInput && (
        <Box sx={{ p: 2 }}>
          <TextField
            fullWidth
            size="small"
            label="Hedef Fiyat"
            type="number"
            value={targetPrice}
            onChange={(e) => setTargetPrice(e.target.value)}
            disabled={loading}
          />
          <Button
            fullWidth
            variant="contained"
            onClick={handlePriceAlertSubmit}
            disabled={loading}
            sx={{ mt: 1 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Fiyat Alarmı Oluştur'}
          </Button>
        </Box>
      )}
      {error && (
        <Alert severity="error" onClose={() => setError(null)} sx={{ m: 2 }}>
          {error}
        </Alert>
      )}
      <Dialog open={isMarketDialogOpen} onClose={() => setIsMarketDialogOpen(false)}>
        <DialogTitle>Market Seçildi</DialogTitle>
        <DialogContent>
          <Typography>
            {selectedMarketId && product.prices.find((p: Price) => p.market_id === selectedMarketId)?.market_name}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsMarketDialogOpen(false)}>Kapat</Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
};

export default ProductCard; 