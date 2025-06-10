import React, { useEffect, useState } from 'react';
import { Container, Grid, Typography, Box, Card, CardContent, CardMedia, Button } from '@mui/material';
import { Favorite, FavoriteBorder, ShoppingCart } from '@mui/icons-material';
import axios from 'axios';
import { ProductDetail } from '../types/product';

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
  const [loading, setLoading] = useState(true);
  const [testDetails, setTestDetails] = useState<ProductWithDetails[]>([]);

  useEffect(() => {
    loadTestDetails();
  }, []);

  const loadTestDetails = async () => {
    try {
      setLoading(true);
      console.log('Loading test details...');
      
      const response = await axios.get('http://localhost:8000/api/v1/products/test-details', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      console.log('Test details response:', response.data);
      
      // Sadece favori olan detayları filtrele
      const favoriteDetails = response.data.sample_details.filter((detail: ProductDetail) => detail.is_favorite);
      console.log('Favorite details:', favoriteDetails);
      
      // Her detay için ürün bilgilerini al
      const detailsWithProducts = await Promise.all(
        favoriteDetails.map(async (detail: ProductDetail) => {
          try {
            const productResponse = await axios.get(`http://localhost:8000/api/v1/products/${detail.product_id}`, {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
              }
            });
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
      
      setTestDetails(detailsWithProducts);
    } catch (error) {
      console.error('Test verileri yüklenirken hata:', error);
      if (axios.isAxiosError(error)) {
        console.error('Error response:', error.response?.data);
        console.error('Error status:', error.response?.status);
      }
      setTestDetails([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container>
        <Typography variant="h5" component="h1" gutterBottom>
          Ürünler
        </Typography>
        <Typography>Yükleniyor...</Typography>
      </Container>
    );
  }

  return (
    <Container>
      <Typography variant="h5" component="h1" gutterBottom>
        Ürünler
      </Typography>
      
      {testDetails.length === 0 ? (
        <Typography>Veri bulunamadı.</Typography>
      ) : (
        <Grid container spacing={3}>
          {testDetails.map((detail) => (
            <Grid item xs={12} sm={6} md={4} key={detail.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                {detail.product?.image_url && (
                  <CardMedia
                    component="img"
                    height="200"
                    image={detail.product.image_url}
                    alt={detail.product.name || `Ürün ${detail.product_id}`}
                  />
                )}
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {detail.product?.name || `Ürün #${detail.product_id}`}
                  </Typography>
                  
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Market: {detail.market?.name || `Market #${detail.market_id}`}
                    </Typography>
                    <Typography variant="h6" color="primary" gutterBottom>
                      {formatPrice(detail.price)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Kalori: {detail.calories} kcal
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Son Kullanma: {new Date(detail.expiration_date).toLocaleDateString('tr-TR')}
                    </Typography>
                  </Box>

                  <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Button
                      variant="contained"
                      color="primary"
                      startIcon={<ShoppingCart />}
                    >
                      Sepete Ekle
                    </Button>
                    <Button
                      color="primary"
                      onClick={() => console.log('Favori tıklandı:', detail.id)}
                    >
                      {detail.is_favorite ? <Favorite color="error" /> : <FavoriteBorder />}
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
