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
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Rating,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  Snackbar,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  ArrowBack,
  Favorite,
  FavoriteBorder,
  AddShoppingCart,
  CompareArrows,
  Comment,
  LocalOffer,
  Notifications,
  NotificationsOff,
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Product } from '../types/product';
import { Market } from '../types/market';
import { ShoppingList } from '../types/shoppingList';
import { Review } from '../types/review';
import { useSnackbar } from 'notistack';

interface PriceHistory {
  date: string;
  price: number;
  market_id: number;
  market_name: string;
}

interface PriceAlert {
  id: number;
  product_id: number;
  user_id: number;
  target_price: number;
  is_active: boolean;
}

const ProductDetail: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [priceHistory, setPriceHistory] = useState<PriceHistory[]>([]);
  const [showAddToListDialog, setShowAddToListDialog] = useState(false);
  const [shoppingLists, setShoppingLists] = useState<ShoppingList[]>([]);
  const [selectedListId, setSelectedListId] = useState<number | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [similarProducts, setSimilarProducts] = useState<Product[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [showReviewDialog, setShowReviewDialog] = useState(false);
  const [newReview, setNewReview] = useState({ rating: 0, content: '' });
  const [priceAlert, setPriceAlert] = useState<PriceAlert | null>(null);
  const [showPriceAlertDialog, setShowPriceAlertDialog] = useState(false);
  const [targetPrice, setTargetPrice] = useState('');
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    const loadProduct = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`http://localhost:8000/api/v1/products/${id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        setProduct(response.data);

        // Fiyat geçmişini getir
        try {
          const historyResponse = await axios.get(`http://localhost:8000/api/v1/products/${id}/price-history`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          setPriceHistory(historyResponse.data);
        } catch (error) {
          console.error('Fiyat geçmişi yüklenirken hata:', error);
        }

        // Benzer ürünleri getir
        try {
          const similarResponse = await axios.get(`http://localhost:8000/api/v1/products/${id}/similar`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          setSimilarProducts(similarResponse.data);
        } catch (error) {
          console.error('Benzer ürünler yüklenirken hata:', error);
        }

        // Fiyat alarmını getir
        try {
          const alertResponse = await axios.get(`http://localhost:8000/api/v1/products/${id}/price-alert`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          setPriceAlert(alertResponse.data);
        } catch (error) {
          console.error('Fiyat alarmı yüklenirken hata:', error);
        }
      } catch (error) {
        console.error('Veri yüklenirken hata:', error);
        enqueueSnackbar('Ürün bilgileri yüklenirken bir hata oluştu', { variant: 'error' });
      } finally {
        setLoading(false);
      }
    };

    loadProduct();
  }, [id]);

  useEffect(() => {
    loadShoppingLists();
  }, []);

  useEffect(() => {
    if (product) {
      loadReviews();
    }
  }, [product]);

  const loadShoppingLists = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/shopping-lists', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      setShoppingLists(response.data);
      if (response.data.length > 0) {
        setSelectedListId(response.data[0].id);
      }
    } catch (error) {
      console.error('Alışveriş listeleri yüklenirken hata:', error);
      enqueueSnackbar('Alışveriş listeleri yüklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const loadReviews = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/v1/comments/product/${product?.id}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      setReviews(response.data);
    } catch (error) {
      console.error('Yorumlar yüklenirken hata:', error);
      enqueueSnackbar('Yorumlar yüklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleToggleFavorite = async () => {
    if (!product) return;

    try {
      const isFavorite = product.is_favorite;
      const endpoint = isFavorite ? 'unfavorite' : 'favorite';
      
      await axios.post(`http://localhost:8000/api/v1/products/${product.id}/${endpoint}`, {}, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      setProduct({ ...product, is_favorite: !isFavorite });
    } catch (error) {
      console.error('Favori işlemi sırasında hata:', error);
    }
  };

  const handleAddToList = async () => {
    if (!selectedListId || !product) return;

    try {
      const response = await axios.post(
        `http://localhost:8000/api/v1/shopping-lists/${selectedListId}/items`,
        {
          product_id: product.id,
          quantity: quantity
        },
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );

      setShowAddToListDialog(false);
      setSnackbar({
        open: true,
        message: 'Ürün listeye eklendi',
        severity: 'success'
      });
    } catch (error) {
      console.error('Ürün listeye eklenirken hata:', error);
      setSnackbar({
        open: true,
        message: 'Ürün listeye eklenirken bir hata oluştu',
        severity: 'error'
      });
    }
  };

  const handleSubmitReview = async () => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/v1/comments',
        {
          product_id: product?.id,
          rating: newReview.rating,
          content: newReview.content
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      setReviews([...reviews, response.data]);
      setNewReview({ rating: 0, content: '' });
      setShowReviewDialog(false);
      enqueueSnackbar('Yorumunuz başarıyla eklendi', { variant: 'success' });
    } catch (error) {
      console.error('Yorum eklenirken hata:', error);
      enqueueSnackbar('Yorum eklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleTogglePriceAlert = async () => {
    if (!product) return;

    try {
      if (priceAlert) {
        // Mevcut alarmı kaldır
        await axios.delete(`http://localhost:8000/api/v1/products/${id}/price-alert`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        setPriceAlert(null);
        setSnackbar({
          open: true,
          message: 'Fiyat alarmı kaldırıldı',
          severity: 'success'
        });
      } else {
        // Yeni alarm oluştur
        setShowPriceAlertDialog(true);
      }
    } catch (error) {
      console.error('Fiyat alarmı işlemi sırasında hata:', error);
      setSnackbar({
        open: true,
        message: 'İşlem sırasında bir hata oluştu',
        severity: 'error'
      });
    }
  };

  const handleCreatePriceAlert = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/api/v1/products/${id}/price-alert`, {
        target_price: parseFloat(targetPrice)
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      setPriceAlert(response.data);
      setShowPriceAlertDialog(false);
      setTargetPrice('');
      setSnackbar({
        open: true,
        message: 'Fiyat alarmı oluşturuldu',
        severity: 'success'
      });
    } catch (error) {
      console.error('Fiyat alarmı oluşturulurken hata:', error);
      setSnackbar({
        open: true,
        message: 'Fiyat alarmı oluşturulurken bir hata oluştu',
        severity: 'error'
      });
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!product) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <Typography variant="h6" color="text.secondary">
          Ürün bulunamadı
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
            Ürün Detayı
          </Typography>
          <IconButton
            color="inherit"
            onClick={handleToggleFavorite}
          >
            {product.is_favorite ? <Favorite /> : <FavoriteBorder />}
          </IconButton>
          <IconButton
            color="inherit"
            onClick={handleTogglePriceAlert}
          >
            {priceAlert ? <Notifications /> : <NotificationsOff />}
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Grid container spacing={3}>
          {/* Ürün Bilgileri */}
          <Grid item xs={12} md={6}>
            <Card>
              <Box
                sx={{
                  height: 400,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  backgroundColor: '#f5f5f5',
                  padding: '1rem'
                }}
              >
                <img
                  src={product.image_url || '/placeholder.png'}
                  alt={product.name}
                  style={{
                    maxWidth: '100%',
                    maxHeight: '100%',
                    objectFit: 'contain'
                  }}
                />
              </Box>
              <CardContent>
                <Typography variant="h4" gutterBottom>
                  {product.name}
                </Typography>
                <Typography variant="body1" color="text.secondary" paragraph>
                  {product.description}
                </Typography>
                {product.details.map((detail) => (
                  <Box key={detail.market_id} sx={{ mb: 2 }}>
                    <Typography variant="h6" color="primary">
                      {detail.price.toLocaleString('tr-TR', {
                        style: 'currency',
                        currency: 'TRY'
                      })}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {detail.market?.name}
                    </Typography>
                    {detail.expiration_date && (
                      <Chip
                        size="small"
                        label={`SKT: ${new Date(detail.expiration_date).toLocaleDateString('tr-TR')}`}
                        color="warning"
                        sx={{ mt: 1 }}
                      />
                    )}
                  </Box>
                ))}
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<AddShoppingCart />}
                  onClick={() => setShowAddToListDialog(true)}
                  sx={{ mt: 2 }}
                >
                  Alışveriş Listesine Ekle
                </Button>
              </CardContent>
            </Card>
          </Grid>

          {/* Fiyat Karşılaştırma ve Geçmiş */}
          <Grid item xs={12} md={6}>
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Fiyat Karşılaştırması
                </Typography>
                <List>
                  {product.details.map((detail) => (
                    <ListItem key={detail.market_id}>
                      <ListItemAvatar>
                        <Avatar src={detail.market?.logo_url} />
                      </ListItemAvatar>
                      <ListItemText
                        primary={detail.market?.name}
                        secondary={detail.price.toLocaleString('tr-TR', {
                          style: 'currency',
                          currency: 'TRY'
                        })}
                      />
                      <Button
                        variant="outlined"
                        size="small"
                        startIcon={<CompareArrows />}
                        onClick={() => navigate(`/markets/${detail.market_id}`)}
                      >
                        Markete Git
                      </Button>
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>

            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Fiyat Geçmişi
                </Typography>
                {/* Burada fiyat geçmişi grafiği olacak */}
                <Box sx={{ height: 200, backgroundColor: '#f5f5f5' }}>
                  {/* Grafik bileşeni eklenecek */}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Yorumlar */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="h6">
                    Yorumlar ve Puanlar
                  </Typography>
                  <Button
                    variant="outlined"
                    startIcon={<Comment />}
                    onClick={() => setShowReviewDialog(true)}
                  >
                    Yorum Yap
                  </Button>
                </Box>
                <List>
                  {reviews.map((review) => (
                    <ListItem key={review.id} divider>
                      <ListItemText
                        primary={
                          <Box display="flex" alignItems="center">
                            <Typography variant="subtitle1" sx={{ mr: 1 }}>
                              {review.user_name}
                            </Typography>
                            <Rating value={review.rating} readOnly size="small" />
                          </Box>
                        }
                        secondary={
                          <>
                            <Typography variant="body2" color="text.secondary">
                              {new Date(review.created_at).toLocaleDateString('tr-TR')}
                            </Typography>
                            <Typography variant="body1" sx={{ mt: 1 }}>
                              {review.content}
                            </Typography>
                          </>
                        }
                      />
                    </ListItem>
                  ))}
                  {reviews.length === 0 && (
                    <Typography variant="body1" color="text.secondary" align="center" sx={{ py: 2 }}>
                      Henüz yorum yapılmamış
                    </Typography>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Benzer Ürünler */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Benzer Ürünler
                </Typography>
                <Grid container spacing={2}>
                  {similarProducts.map((similarProduct) => (
                    <Grid item xs={12} sm={6} md={4} key={similarProduct.id}>
                      <Card
                        sx={{
                          cursor: 'pointer',
                          '&:hover': {
                            boxShadow: 6,
                            transform: 'translateY(-4px)',
                            transition: 'all 0.3s ease-in-out'
                          }
                        }}
                        onClick={() => navigate(`/products/${similarProduct.id}`)}
                      >
                        <Box
                          sx={{
                            height: 140,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            backgroundColor: '#f5f5f5',
                            padding: '1rem'
                          }}
                        >
                          <img
                            src={similarProduct.image_url || '/placeholder.png'}
                            alt={similarProduct.name}
                            style={{
                              maxWidth: '100%',
                              maxHeight: '100%',
                              objectFit: 'contain'
                            }}
                          />
                        </Box>
                        <CardContent>
                          <Typography variant="h6" noWrap>
                            {similarProduct.name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" noWrap>
                            {similarProduct.description}
                          </Typography>
                          <Typography variant="h6" color="primary">
                            {similarProduct.details[0]?.price.toLocaleString('tr-TR', {
                              style: 'currency',
                              currency: 'TRY'
                            })}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>

      {/* Alışveriş Listesine Ekle Dialog'u */}
      <Dialog open={showAddToListDialog} onClose={() => setShowAddToListDialog(false)}>
        <DialogTitle>Alışveriş Listesine Ekle</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>Liste Seçin</InputLabel>
            <Select
              value={selectedListId || ''}
              onChange={(e) => setSelectedListId(Number(e.target.value))}
              label="Liste Seçin"
            >
              {shoppingLists.map((list) => (
                <MenuItem key={list.id} value={list.id}>
                  {list.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            fullWidth
            type="number"
            label="Adet"
            value={quantity}
            onChange={(e) => setQuantity(Number(e.target.value))}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAddToListDialog(false)}>İptal</Button>
          <Button onClick={handleAddToList} variant="contained">
            Ekle
          </Button>
        </DialogActions>
      </Dialog>

      {/* Yorum Yapma Dialog'u */}
      <Dialog open={showReviewDialog} onClose={() => setShowReviewDialog(false)}>
        <DialogTitle>Yorum Yap</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Typography component="legend">Puanınız</Typography>
            <Rating
              value={newReview.rating}
              onChange={(_, value) => setNewReview({ ...newReview, rating: value || 0 })}
              precision={0.5}
            />
          </Box>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Yorumunuz"
            value={newReview.content}
            onChange={(e) => setNewReview({ ...newReview, content: e.target.value })}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowReviewDialog(false)}>İptal</Button>
          <Button
            onClick={handleSubmitReview}
            variant="contained"
            disabled={newReview.rating === 0}
          >
            Gönder
          </Button>
        </DialogActions>
      </Dialog>

      {/* Fiyat Alarmı Dialog'u */}
      <Dialog open={showPriceAlertDialog} onClose={() => setShowPriceAlertDialog(false)}>
        <DialogTitle>Fiyat Alarmı Oluştur</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Hedef Fiyat"
            type="number"
            fullWidth
            value={targetPrice}
            onChange={(e) => setTargetPrice(e.target.value)}
            InputProps={{
              startAdornment: <Typography sx={{ mr: 1 }}>₺</Typography>
            }}
          />
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
            Ürün fiyatı bu değerin altına düştüğünde size bildirim göndereceğiz.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowPriceAlertDialog(false)}>İptal</Button>
          <Button onClick={handleCreatePriceAlert} variant="contained">
            Alarm Oluştur
          </Button>
        </DialogActions>
      </Dialog>

      {/* Bildirim Snackbar'ı */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </>
  );
};

export default ProductDetail; 