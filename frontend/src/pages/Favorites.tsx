import React, { useEffect, useState } from 'react';
import { Container, Grid, Typography, Box, Card, CardContent, CardMedia, Button, CircularProgress } from '@mui/material';
import { Favorite, FavoriteBorder, ShoppingCart } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import favoriteService from '../services/favorite';
import { ProductDetail } from '../types/product';
import { useAuth } from '../contexts/AuthContext';

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('tr-TR', {
    style: 'currency',
    currency: 'TRY'
  }).format(price);
};

interface ProductWithDetails extends ProductDetail {
  product?: {
    id: number;
    name: string;
    description: string;
    image_url?: string;
    category_id: number;
    created_at: string;
    updated_at: string;
    details: ProductDetail[];
    is_favorite?: boolean;
  };
}

const Favorites: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [favorites, setFavorites] = useState<ProductWithDetails[]>([]);

  useEffect(() => {
    if (!user) {
      navigate('/login', { state: { from: '/favorites' } });
    }
  }, [user, navigate]);

  useEffect(() => {
    loadFavorites();
  }, []);

  const loadFavorites = async () => {
    try {
      setLoading(true);
      const favoritesData = await favoriteService.getFavorites();
      setFavorites(favoritesData);
    } catch (error) {
      console.error('Favoriler yüklenirken hata:', error);
      setFavorites([]);
    } finally {
      setLoading(false);
    }
  };

  const handleFavoriteClick = async (productId: number, marketId: number) => {
    try {
      await favoriteService.removeFavorite(productId, marketId);
      loadFavorites(); // Favorileri yeniden yükle
    } catch (error) {
      console.error('Favori durumu değiştirilirken hata:', error);
    }
  };

  if (loading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mt: 4, mb: 4 }}>
        Favorilerim
      </Typography>

      {favorites.length === 0 ? (
        <Typography variant="h6" align="center" color="textSecondary">
          Henüz favori ürününüz bulunmuyor.
        </Typography>
      ) : (
        <Grid container spacing={3}>
          {favorites.map((favorite) => (
            <Grid item xs={12} sm={6} md={4} key={favorite.id}>
              <Card>
                <CardMedia
                  component="img"
                  height="200"
                  image={favorite.product?.image_url || '/placeholder.png'}
                  alt={favorite.product?.name}
                  sx={{ objectFit: 'contain', p: 2 }}
                />
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {favorite.product?.name}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    {favorite.product?.description}
                  </Typography>
                  <Typography variant="h6" color="primary" gutterBottom>
                    {formatPrice(favorite.price)}
                  </Typography>

                  <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Button
                      variant="contained"
                      color="primary"
                      startIcon={<ShoppingCart />}
                      onClick={() => navigate(`/products/${favorite.product_id}`)}
                    >
                      Detayları Gör
                    </Button>
                    <Button
                      color="primary"
                      onClick={() => handleFavoriteClick(favorite.product_id, favorite.market_id)}
                    >
                      <Favorite color="error" />
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default Favorites;
