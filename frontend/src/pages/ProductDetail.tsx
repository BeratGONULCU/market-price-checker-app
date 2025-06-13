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
  Add as AddIcon,
  ShoppingCart as ShoppingCartIcon,
  List as ListIcon
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Product } from '../types/product';
import type { ProductDetail as ProductDetailType } from '../types/product';
import { Market } from '../types/market';
import { ShoppingList } from '../types';
import { Review } from '../types/review';
import { useSnackbar } from 'notistack';
import favoriteService from '../services/favorite';
import shoppingListService from '../services/shoppingList';

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
  const [selectedList, setSelectedList] = useState<number | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [similarProducts, setSimilarProducts] = useState<Product[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [showReviewDialog, setShowReviewDialog] = useState(false);
  const [reviewRating, setReviewRating] = useState(0);
  const [reviewContent, setReviewContent] = useState('');
  const [priceAlert, setPriceAlert] = useState<PriceAlert | null>(null);
  const [showPriceAlertDialog, setShowPriceAlertDialog] = useState(false);
  const [targetPrice, setTargetPrice] = useState('');
  const { enqueueSnackbar } = useSnackbar();
  const [openListDialog, setOpenListDialog] = useState(false);
  const [notes, setNotes] = useState('');

  const fetchProductDetails = async () => {
    if (!id) return;
    
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/api/v1/products/${id}`);
      console.log('Product Response:', response.data);
      console.log('Product Details:', response.data.details);
      setProduct(response.data);
      
      // Market detaylarını kontrol et
      if (response.data.details) {
        console.log('Market details:', response.data.details.map((detail: ProductDetailType) => ({
          market_id: detail.market_id,
          market_name: detail.market?.name,
          price: detail.price
        })));
      }

      // Fiyat geçmişini getir - geçici olarak devre dışı bırakıldı
      // const historyResponse = await axios.get(`http://localhost:8000/api/v1/products/${id}/price-history`);
      // setPriceHistory(historyResponse.data);

      // Benzer ürünleri getir
      const similarResponse = await axios.get(`http://localhost:8000/api/v1/products/${id}/similar`);
      setSimilarProducts(similarResponse.data);

      // Yorumları getir
      const reviewsResponse = await axios.get(`http://localhost:8000/api/v1/comments/product/${id}`);
      setReviews(reviewsResponse.data);

      // Alışveriş listelerini getir
      const listsResponse = await axios.get('http://localhost:8000/api/v1/shopping-lists', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      setShoppingLists(listsResponse.data);
      if (listsResponse.data.length > 0) {
        setSelectedList(listsResponse.data[0].id);
      }
    } catch (error) {
      console.error('Error fetching product details:', error);
      enqueueSnackbar('Ürün detayları yüklenirken bir hata oluştu', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProductDetails();
  }, [id]);

  const handleToggleFavorite = async () => {
    if (!product) return;

    try {
      const isFavorite = product.is_favorite;
      
      if (isFavorite) {
        // En düşük fiyatlı marketi seç
        const lowestPriceDetail = product.details.reduce((prev, current) => 
          (prev.price < current.price) ? prev : current
        );
        await favoriteService.removeFavorite(product.id, lowestPriceDetail.market_id);
      } else {
        // En düşük fiyatlı marketi seç
        const lowestPriceDetail = product.details.reduce((prev, current) => 
          (prev.price < current.price) ? prev : current
        );
        await favoriteService.addFavorite(product.id, lowestPriceDetail.market_id);
      }

      // Ürün durumunu güncelle
      setProduct({ ...product, is_favorite: !isFavorite });
      enqueueSnackbar(
        isFavorite ? 'Ürün favorilerden çıkarıldı' : 'Ürün favorilere eklendi',
        { variant: 'success' }
      );
    } catch (error) {
      console.error('Favori işlemi sırasında hata:', error);
      enqueueSnackbar('Favori işlemi sırasında bir hata oluştu', { variant: 'error' });
    }
  };

  const loadShoppingLists = async () => {
    try {
      const lists = await shoppingListService.getLists();
      setShoppingLists(lists);
      if (lists.length > 0) {
        setSelectedList(lists[0].id);
      }
    } catch (error) {
      console.error('Error loading shopping lists:', error);
      enqueueSnackbar('Alışveriş listeleri yüklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleAddToList = async () => {
    if (!selectedList || !product) return;
    try {
      await shoppingListService.addItem(selectedList, product.id, quantity);
      setOpenListDialog(false);
      setQuantity(1);
      setNotes('');
      enqueueSnackbar('Ürün listeye eklendi', { variant: 'success' });
    } catch (error) {
      console.error('Error adding to list:', error);
      enqueueSnackbar('Ürün listeye eklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleOpenListDialog = () => {
    loadShoppingLists();
    setOpenListDialog(true);
  };

  const handleCloseListDialog = () => {
    setOpenListDialog(false);
    setQuantity(1);
    setNotes('');
    setSelectedList(null);
  };

  const handleSubmitReview = async () => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            enqueueSnackbar('Yorum yapmak için giriş yapmalısınız', { variant: 'error' });
            return;
        }

        const reviewData = {
            product_id: product?.id,
            rating: reviewRating,
            content: reviewContent
        };

        console.log('Sending review data:', reviewData);
        console.log('Request headers:', {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        });

        const response = await axios.post(
            'http://localhost:8000/api/v1/comments',
            reviewData,
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );

        console.log('Review response:', response);
        console.log('Response status:', response.status);
        console.log('Response data:', response.data);

        if (response.status === 201) {
            enqueueSnackbar('Yorumunuz başarıyla eklendi', { variant: 'success' });
            setReviewRating(0);
            setReviewContent('');
            setShowReviewDialog(false);
            // Yorumları yenile
            fetchProductDetails();
        }
    } catch (error: any) {
        console.error('Error submitting review:', error);
        console.error('Error details:', {
            message: error.message,
            response: error.response?.data,
            status: error.response?.status,
            headers: error.response?.headers
        });
        
        if (error.response) {
            console.error('Error response:', error.response.data);
            enqueueSnackbar(error.response.data.detail || 'Yorum eklenirken bir hata oluştu', { variant: 'error' });
        } else {
            enqueueSnackbar('Yorum eklenirken bir hata oluştu', { variant: 'error' });
        }
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
        enqueueSnackbar('Fiyat alarmı kaldırıldı', { variant: 'success' });
      } else {
        // Yeni alarm oluştur
        setShowPriceAlertDialog(true);
      }
    } catch (error) {
      console.error('Fiyat alarmı işlemi sırasında hata:', error);
      enqueueSnackbar('İşlem sırasında bir hata oluştu', { variant: 'error' });
    }
  };

  const handleCreatePriceAlert = async () => {
    try {
      const response = await axios.post(
        `http://localhost:8000/api/v1/products/${product?.id}/price-alert`,
        {
          target_price: targetPrice
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      );

      setPriceAlert(response.data);
      setShowPriceAlertDialog(false);
      setTargetPrice('');
      enqueueSnackbar('Fiyat alarmı başarıyla oluşturuldu', { variant: 'success' });
    } catch (error) {
      console.error('Error creating price alert:', error);
      enqueueSnackbar('Fiyat alarmı oluşturulurken bir hata oluştu', { variant: 'error' });
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!product) {
    return (
      <Typography variant="h6" align="center">
          Ürün bulunamadı
        </Typography>
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
                <Box display="flex" gap={2} mt={2}>
                <Button
                  variant="contained"
                  color="primary"
                    startIcon={<ShoppingCartIcon />}
                  onClick={() => setShowAddToListDialog(true)}
                  >
                    Listeye Ekle
                  </Button>
                  <Button
                    variant="outlined"
                    color="primary"
                    startIcon={<ListIcon />}
                    onClick={handleOpenListDialog}
                >
                    Listeye Ekle
                </Button>
                  <IconButton
                    color="primary"
                    onClick={handleToggleFavorite}
                    sx={{ ml: 'auto' }}
                  >
                    {product.is_favorite ? <Favorite /> : <FavoriteBorder />}
                  </IconButton>
                </Box>
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
                        primary={
                          <Box sx={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            justifyContent: 'space-between',
                            width: '100%'
                          }}>
                            <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                              {detail.market?.name || 'Bilinmeyen Market'}
                            </Typography>
                            <Typography variant="subtitle1" color="primary" sx={{ mr: 3.75 }}>
                              {detail.price.toLocaleString('tr-TR', {
                                style: 'currency',
                                currency: 'TRY'
                              })}
                            </Typography>
                          </Box>
                        }
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
          {similarProducts.length > 0 && (
            <Box mt={6}>
              <Typography variant="h5" gutterBottom>
                  Benzer Ürünler
                </Typography>
              <Grid container spacing={3}>
                  {similarProducts.map((similarProduct) => (
                    <Grid item xs={12} sm={6} md={4} key={similarProduct.id}>
                    <Card>
                      <CardContent>
                        <Box
                          component="img"
                          src={similarProduct.image_url || '/placeholder.png'}
                          alt={similarProduct.name}
                          sx={{
                            width: '100%',
                            height: 200,
                            objectFit: 'contain',
                            mb: 2
                            }}
                          />
                        <Typography variant="h6" gutterBottom>
                            {similarProduct.name}
                          </Typography>
                        <Typography variant="body2" color="textSecondary" paragraph>
                            {similarProduct.description}
                          </Typography>
                        {similarProduct.details && similarProduct.details.length > 0 && (
                          <Typography variant="h6" color="primary">
                            {new Intl.NumberFormat('tr-TR', {
                              style: 'currency',
                              currency: 'TRY'
                            }).format(similarProduct.details[0].price)}
                          </Typography>
                        )}
                        <Button
                          variant="contained"
                          color="primary"
                          fullWidth
                          sx={{ mt: 2 }}
                          onClick={() => navigate(`/products/${similarProduct.id}`)}
                        >
                          Detayları Gör
                        </Button>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
            </Box>
          )}
        </Grid>
      </Container>

      {/* Alışveriş Listesine Ekle Dialog'u */}
      <Dialog open={showAddToListDialog} onClose={() => setShowAddToListDialog(false)}>
        <DialogTitle>Alışveriş Listesine Ekle</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>Liste Seçin</InputLabel>
            <Select
              value={selectedList || ''}
              onChange={(e) => setSelectedList(Number(e.target.value))}
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
          <Button onClick={() => handleAddToList()} variant="contained">
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
              value={reviewRating}
              onChange={(_, value) => setReviewRating(value || 0)}
              precision={0.5}
            />
          </Box>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Yorumunuz"
            value={reviewContent}
            onChange={(e) => setReviewContent(e.target.value)}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowReviewDialog(false)}>İptal</Button>
          <Button
            onClick={handleSubmitReview}
            variant="contained"
            disabled={reviewRating === 0}
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

      {/* Listeye Ekle Dialog */}
      <Dialog open={openListDialog} onClose={handleCloseListDialog}>
        <DialogTitle>Listeye Ekle</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="normal">
            <InputLabel>Liste Seçin</InputLabel>
            <Select
              value={selectedList || ''}
              onChange={(e) => setSelectedList(Number(e.target.value))}
            >
              {shoppingLists.map((list) => (
                <MenuItem key={list.id} value={list.id}>
                  {list.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin="normal"
            label="Miktar"
            type="number"
            fullWidth
            value={quantity}
            onChange={(e) => setQuantity(Number(e.target.value))}
            inputProps={{ min: 1 }}
          />
          <TextField
            margin="normal"
            label="Notlar"
            multiline
            rows={2}
            fullWidth
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseListDialog}>İptal</Button>
          <Button
            onClick={handleAddToList}
            color="primary"
            disabled={!selectedList || quantity < 1}
          >
            Ekle
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default ProductDetail; 