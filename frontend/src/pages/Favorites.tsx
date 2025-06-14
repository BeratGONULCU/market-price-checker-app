import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Box,
  CircularProgress,
  Card,
  CardContent,
  CardMedia,
  IconButton
} from '@mui/material';
import { useSnackbar } from 'notistack';
import { Favorite, FavoriteBorder } from '@mui/icons-material';
import { ProductDetail } from '../types';
import axios from 'axios';

const Favorites: React.FC = () => {
  const [favorites, setFavorites] = useState<ProductDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    fetchFavorites();
  }, []);

  const fetchFavorites = async () => {
    try {
      setLoading(true);
      console.log('Fetching favorites...');
      const response = await axios.get('http://localhost:8000/api/v1/favorites');
      console.log('Favorites response:', response.data);

      // Her detay için ürün bilgilerini al
      const detailsWithProducts = await Promise.all(
        response.data.map(async (detail: ProductDetail) => {
          try {
            const productResponse = await axios.get(`http://localhost:8000/api/v1/products/${detail.product_id}`);
            return {
              ...detail,
              product: productResponse.data
            };
          } catch (error) {
            console.error(`Error fetching product ${detail.product_id}:`, error);
            return detail;
          }
        })
      );

      setFavorites(detailsWithProducts);
    } catch (error) {
      console.error('Error fetching favorites:', error);
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        enqueueSnackbar(`Hata: ${error.response.data.detail}`, { variant: 'error' });
      } else {
        enqueueSnackbar('Favoriler yüklenirken bir hata oluştu', { variant: 'error' });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleToggleFavorite = async (detailId: number) => {
    try {
      await axios.post(`http://localhost:8000/api/v1/favorites/toggle/${detailId}`);

      // Favorileri güncelle
      setFavorites(prev =>
        prev.map(detail =>
          detail.id === detailId
            ? { ...detail, is_favorite: !detail.is_favorite }
            : detail
        )
      );

      // Favori kaldırıldıysa listeden çıkar
      setFavorites(prev => prev.filter(detail => detail.is_favorite));
    } catch (error) {
      console.error('Favori güncellenemedi:', error);
      enqueueSnackbar('Favori güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Favorilerim
      </Typography>

      {favorites.length === 0 ? (
        <Typography variant="body1" color="text.secondary" align="center" sx={{ mt: 4 }}>
          Henüz favori ürününüz bulunmamaktadır.
        </Typography>
      ) : (
        <Grid container spacing={3}>
          {favorites.map((detail) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={detail.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={detail.product?.image_url || 'https://via.placeholder.com/200'}
                  alt={detail.product?.name || 'Ürün'}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h6" component="h2">
                    {detail.product?.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {detail.product?.description}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="h6" color="primary">
                      {detail.price?.toLocaleString('tr-TR', {
                        style: 'currency',
                        currency: 'TRY'
                      })}
                    </Typography>
                    <Box>
                      <IconButton
                        onClick={() => handleToggleFavorite(detail.id)}
                        color={detail.is_favorite ? 'error' : 'default'}
                      >
                        {detail.is_favorite ? <Favorite /> : <FavoriteBorder />}
                      </IconButton>
                    </Box>
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {detail.market?.name}
                  </Typography>
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
