import React, { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  AppBar,
  Toolbar,
  IconButton,
  CircularProgress,
} from '@mui/material';
import {
  ArrowBack,
  LocationOn,
  Phone,
  AccessTime,
  Directions,
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Market } from '../types/market';

const MarketDetail: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [market, setMarket] = useState<Market | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMarket = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`http://localhost:8000/api/v1/markets/${id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        console.log('Market data:', response.data);
        setMarket(response.data);
      } catch (error) {
        console.error('Market yüklenirken hata:', error);
      } finally {
        setLoading(false);
      }
    };

    loadMarket();
  }, [id]);

  const handleGetDirections = () => {
    if (market?.latitude && market?.longitude) {
      const url = `https://www.google.com/maps/dir/?api=1&destination=${market.latitude},${market.longitude}`;
      window.open(url, '_blank');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!market) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <Typography variant="h6" color="text.secondary">
          Market bulunamadı
        </Typography>
      </Box>
    );
  }

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            onClick={() => navigate(-1)}
            sx={{ mr: 2 }}
          >
            <ArrowBack />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Market Detayı
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Grid container spacing={3}>
          {/* Market Bilgileri */}
          <Grid item xs={12} md={4}>
            <Card>
              <Box
                sx={{
                  height: 200,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  backgroundColor: '#f5f5f5',
                  padding: '1rem'
                }}
              >
                <img
                  src={market.image_url || '/placeholder.png'}
                  alt={market.name}
                  style={{
                    maxWidth: '100%',
                    maxHeight: '100%',
                    objectFit: 'contain'
                  }}
                />
              </Box>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  {market.name}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <LocationOn color="action" sx={{ mr: 1 }} />
                  <Typography variant="body2" color="text.secondary">
                    {market.address}
                  </Typography>
                </Box>
                {market.phone && (
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Phone color="action" sx={{ mr: 1 }} />
                    <Typography variant="body2" color="text.secondary">
                      {market.phone}
                    </Typography>
                  </Box>
                )}
                {market.open_hours && (
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <AccessTime color="action" sx={{ mr: 1 }} />
                    <Typography variant="body2" color="text.secondary">
                      {market.open_hours}
                    </Typography>
                  </Box>
                )}
                <Button
                  variant="contained"
                  startIcon={<Directions />}
                  fullWidth
                  onClick={handleGetDirections}
                  disabled={!market.latitude || !market.longitude}
                >
                  Yol Tarifi Al
                </Button>
              </CardContent>
            </Card>
          </Grid>

          {/* Ürün Listesi - Bu kısım daha sonra eklenecek */}
          <Grid item xs={12} md={8}>
            <Typography variant="h6" gutterBottom>
              Ürünler
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Ürün listesi yakında eklenecek...
            </Typography>
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default MarketDetail; 