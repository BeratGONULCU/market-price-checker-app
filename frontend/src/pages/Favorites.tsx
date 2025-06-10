import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Box,
  IconButton,
  CircularProgress,
  Button,
} from '@mui/material';
import { Favorite, CompareArrows } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { productService, Product, ProductDetail } from '../services/product';
import { Market } from '../types/market';
import axios from 'axios';

const Favorites: React.FC = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFavoriteProducts();
  }, []);

  const loadFavoriteProducts = async () => {
    try {
      setLoading(true);
      console.log('Loading favorite products...');
      
      // Tüm ürün detaylarını al
      const response = await axios.get('/api/v1/products/product-details', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      console.log('Product details response:', response.data);

      // Favori olan detayları filtrele
      const favoriteDetails = response.data.sample_details.filter((detail: ProductDetail) => detail.is_favorite);
      console.log('Favorite details:', favoriteDetails);

      // Ürünleri grupla
      const productsMap = new Map<number, Product>();
      
      for (const detail of favoriteDetails) {
        if (!productsMap.has(detail.product_id)) {
          // Ürün bilgilerini al
          const productResponse = await axios.get(`/api/v1/products/${detail.product_id}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          
          productsMap.set(detail.product_id, {
            ...productResponse.data,
            details: []
          });
        }
        productsMap.get(detail.product_id)?.details.push(detail);
      }

      const favoriteProducts = Array.from(productsMap.values());
      console.log('Favorite products:', favoriteProducts);
      setProducts(favoriteProducts);
    } catch (error) {
      console.error('Favori ürünler yüklenirken hata:', error);
      if (axios.isAxiosError(error)) {
        console.error('Error response:', error.response?.data);
        console.error('Error status:', error.response?.status);
      }
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveFavorite = async (productId: number, marketId: number) => {
    try {
      console.log('Toggling favorite for product:', productId, 'market:', marketId);
      await axios.patch(`/api/v1/products/${productId}/details/${marketId}/favorite`, {}, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      loadFavoriteProducts();
    } catch (error) {
      console.error('Favori durumu değiştirilirken hata:', error);
    }
  };

  const handleCompare = (product: Product) => {
    navigate('/compare', { state: { product } });
  };

  const formatPrice = (price: number | null) => {
    if (price === null) return 'Fiyat bilgisi yok';
    return price.toLocaleString('tr-TR', {
      style: 'currency',
      currency: 'TRY',
    });
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" sx={{ mt: 4, mb: 4 }}>
        Favorilerim
      </Typography>

      {products.length === 0 ? (
        <Typography variant="h6" color="text.secondary">
          Henüz favori ürününüz bulunmuyor.
        </Typography>
      ) : (
        <Grid container spacing={3}>
          {products.map((product) => (
            <Grid item xs={12} sm={6} md={4} key={product.id}>
              <Card>
                {product.image_url && (
                  <CardMedia
                    component="img"
                    height="140"
                    image={product.image_url}
                    alt={product.name}
                  />
                )}
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {product.name}
                  </Typography>
                  <Typography color="text.secondary" gutterBottom>
                    {product.description}
                  </Typography>
                  {product.details.map((detail) => (
                    <Box key={detail.id} sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Market: {detail.market.name}
                      </Typography>
                      <Typography variant="h6" color="primary">
                        {formatPrice(detail.price)}
                      </Typography>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                        <IconButton 
                          onClick={() => handleRemoveFavorite(product.id, detail.market_id)}
                          color="error"
                        >
                          <Favorite />
                        </IconButton>
                        <Button
                          variant="contained"
                          startIcon={<CompareArrows />}
                          onClick={() => handleCompare(product)}
                        >
                          Karşılaştır
                        </Button>
                      </Box>
                    </Box>
                  ))}
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
