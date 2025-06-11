import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Box,
  Button,
  CircularProgress,
  AppBar,
  Toolbar,
  IconButton,
} from '@mui/material';
import { LocationOn, ShoppingCart, Logout } from '@mui/icons-material';
import axios from 'axios';
import { Market } from '../types/market';

const Markets: React.FC = () => {
  const navigate = useNavigate();
  const [markets, setMarkets] = useState<Market[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMarkets();
  }, []);

  const loadMarkets = async () => {
    try {
      setLoading(true);
      console.log('Fetching markets...');
      const response = await axios.get('http://localhost:8000/api/v1/markets', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      console.log('Markets API Response:', response);
      console.log('Markets Data:', response.data);
      console.log('First Market:', response.data[0]);
      console.log('First Market Image URL:', response.data[0]?.image_url);
      setMarkets(response.data);
    } catch (error) {
      console.error('Markets yüklenirken hata:', error);
      if (axios.isAxiosError(error)) {
        console.error('Error response:', error.response?.data);
        console.error('Error status:', error.response?.status);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleMarketClick = (marketId: number) => {
    navigate(`/markets/${marketId}`);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Marketler
          </Typography>
          <IconButton color="inherit" onClick={() => navigate('/cart')}>
            <ShoppingCart />
          </IconButton>
          <Button color="inherit" onClick={handleLogout}>
            Çıkış Yap
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Marketler
        </Typography>

        {markets.length === 0 ? (
          <Typography variant="h6" color="text.secondary" align="center">
            Market bulunamadı
          </Typography>
        ) : (
          <Grid container spacing={3}>
            {markets.map((market) => {
              console.log('Rendering market:', market);
              const imageUrl = market.image_url
                ? (market.image_url.startsWith('http')
                    ? market.image_url
                    : `http://localhost:8000/static/markets/${market.image_url}`)
                : null;
              console.log('Market image URL:', imageUrl);
              return (
                <Grid item key={market.id} xs={12} sm={6} md={4}>
                  <Card 
                    sx={{ 
                      height: '100%', 
                      display: 'flex', 
                      flexDirection: 'column',
                      cursor: 'pointer',
                      '&:hover': {
                        boxShadow: 6,
                      },
                    }}
                    onClick={() => handleMarketClick(market.id)}
                  >
                    <CardMedia
                      component="img"
                      height="200"
                      image={market.image_url || '/placeholder.png'}
                      alt={market.name}
                    />
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Typography gutterBottom variant="h5" component="h2">
                        {market.name}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <LocationOn color="action" sx={{ mr: 1 }} />
                        <Typography variant="body2" color="text.secondary">
                          {market.address}
                        </Typography>
                      </Box>
                      {market.phone && (
                        <Typography variant="body2" color="text.secondary">
                          Tel: {market.phone}
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              );
            })}
          </Grid>
        )}
      </Container>
    </>
  );
};

export default Markets; 