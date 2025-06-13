import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Box,
  CircularProgress
} from '@mui/material';
import { useSnackbar } from 'notistack';
import ProductCard from '../components/ProductCard';
import { Product } from '../types';
import api from '../services/api';
import { AxiosError } from 'axios';

const Favorites: React.FC = () => {
  const [favorites, setFavorites] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    fetchFavorites();
  }, []);

  const fetchFavorites = async () => {
    try {
      setLoading(true);
      console.log('Fetching favorites...');
      const response = await api.get('/api/favorites');
      console.log('Favorites response:', response.data);
      setFavorites(response.data);
    } catch (error) {
      console.error('Error fetching favorites:', error);
      if (error instanceof AxiosError && error.response?.data?.detail) {
        enqueueSnackbar(`Hata: ${error.response.data.detail}`, { variant: 'error' });
      } else {
        enqueueSnackbar('Favoriler yüklenirken bir hata oluştu', { variant: 'error' });
      }
    } finally {
      setLoading(false);
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
          {favorites.map((product) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={product.id}>
              <ProductCard product={product} />
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default Favorites;
