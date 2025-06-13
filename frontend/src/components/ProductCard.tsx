import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  Box,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress
} from '@mui/material';
import { Favorite, FavoriteBorder, Notifications, NotificationsActive } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { Product, ProductDetail } from '../types';
import { useNavigate } from 'react-router-dom';
import favoriteService from '../services/favorite';
import priceAlertService from '../services/priceAlert';

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const [isFavorite, setIsFavorite] = useState(false);
  const [hasPriceAlert, setHasPriceAlert] = useState(false);
  const [loading, setLoading] = useState(false);
  const [openPriceAlertDialog, setOpenPriceAlertDialog] = useState(false);
  const [targetPrice, setTargetPrice] = useState('');
  const [selectedMarketId, setSelectedMarketId] = useState<number | null>(null);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      checkFavoriteStatus();
      checkPriceAlertStatus();
    }
  }, [user, product]);

  const checkFavoriteStatus = async () => {
    if (!user) return;
    try {
      // En düşük fiyatlı marketi seç
      const lowestPriceDetail = product.details.reduce((prev: ProductDetail, current: ProductDetail) => 
        (prev.price < current.price) ? prev : current
      );
      const status = await favoriteService.isFavorite(product.id, lowestPriceDetail.market_id);
      setIsFavorite(status);
    } catch (error) {
      console.error('Error checking favorite status:', error);
    }
  };

  const checkPriceAlertStatus = async () => {
    if (!user) return;
    try {
      const alert = await priceAlertService.getProductPriceAlert(product.id);
      setHasPriceAlert(!!alert);
    } catch (error) {
      console.error('Error checking price alert status:', error);
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
      const lowestPriceDetail = product.details.reduce((prev: ProductDetail, current: ProductDetail) => 
        (prev.price < current.price) ? prev : current
      );

      console.log('Product details:', product.details);
      console.log('Lowest price detail:', lowestPriceDetail);
      console.log('Toggling favorite for product:', product.id, 'market:', lowestPriceDetail.market_id);

      if (isFavorite) {
        await favoriteService.removeFavorite(product.id, lowestPriceDetail.market_id);
      } else {
        await favoriteService.addFavorite(product.id, lowestPriceDetail.market_id);
      }

      setIsFavorite(!isFavorite);
    } catch (error) {
      console.error('Error toggling favorite:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTogglePriceAlert = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    if (hasPriceAlert) {
      try {
        const alert = await priceAlertService.getProductPriceAlert(product.id);
        if (alert) {
          await priceAlertService.deletePriceAlert(alert.id);
          setHasPriceAlert(false);
        }
      } catch (error) {
        console.error('Error removing price alert:', error);
      }
    } else {
      setOpenPriceAlertDialog(true);
    }
  };

  const handleCreatePriceAlert = async () => {
    if (!selectedMarketId || !targetPrice) return;

    try {
      await priceAlertService.createPriceAlert(product.id, parseFloat(targetPrice));
      setHasPriceAlert(true);
      setOpenPriceAlertDialog(false);
      setTargetPrice('');
      setSelectedMarketId(null);
    } catch (error) {
      console.error('Error creating price alert:', error);
    }
  };

  return (
    <Card sx={{ maxWidth: 345, height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardMedia
        component="img"
        height="140"
        image={product.image_url || 'https://via.placeholder.com/140'}
        alt={product.name}
        sx={{ objectFit: 'contain', p: 2 }}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography gutterBottom variant="h6" component="div" noWrap>
          {product.name}
        </Typography>
        <Box sx={{ mt: 2 }}>
          {product.details.map((detail) => (
            <Button
              key={detail.market_id}
              variant="outlined"
              size="small"
              sx={{ mr: 1, mb: 1 }}
              onClick={() => {
                setSelectedMarketId(detail.market_id);
                setOpenPriceAlertDialog(true);
              }}
            >
              {detail.market?.name}: {detail.price} TL
            </Button>
          ))}
        </Box>
      </CardContent>
      <Box sx={{ p: 2, pt: 0 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <IconButton
            onClick={handleToggleFavorite}
            disabled={loading}
            color={isFavorite ? 'primary' : 'default'}
          >
            {isFavorite ? <Favorite /> : <FavoriteBorder />}
          </IconButton>
          <IconButton
            onClick={handleTogglePriceAlert}
            color={hasPriceAlert ? 'primary' : 'default'}
          >
            {hasPriceAlert ? <NotificationsActive /> : <Notifications />}
          </IconButton>
        </Box>
      </Box>

      <Dialog open={openPriceAlertDialog} onClose={() => setOpenPriceAlertDialog(false)}>
        <DialogTitle>Fiyat Alarmı Oluştur</DialogTitle>
        <DialogContent>
          <Typography>
            {selectedMarketId && product.details.find((d) => d.market_id === selectedMarketId)?.market?.name}
          </Typography>
          <TextField
            fullWidth
            label="Hedef Fiyat"
            type="number"
            value={targetPrice}
            onChange={(e) => setTargetPrice(e.target.value)}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenPriceAlertDialog(false)}>İptal</Button>
          <Button onClick={handleCreatePriceAlert} color="primary">
            Oluştur
          </Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
};

export default ProductCard; 