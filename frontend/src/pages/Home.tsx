import React, { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Box,
  IconButton,
  CircularProgress,
  Modal,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  AppBar,
  Toolbar,
  Button,
  Chip,
  Snackbar,
  Alert,
} from '@mui/material';
import { FavoriteBorder, CompareArrows, Close, Favorite, Logout, ShoppingCart } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { productService, Product, ProductDetail } from '../services/product';
import { categoryService, Category } from '../services/category';
import authService from '../services/auth';
import { Market } from '../types/market';
import axios from 'axios';
import favoriteService from '../services/favorite';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<number | ''>('');
  const [sortBy, setSortBy] = useState('name');
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [openModal, setOpenModal] = useState(false);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [testDetails, setTestDetails] = useState<ProductDetail[]>([]);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error'
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching initial data...');
        const [productsData, categoriesData] = await Promise.all([
          productService.getAllProducts(),
          categoryService.getAllCategories(),
        ]);
        console.log('Fetched Products:', productsData);
        console.log('Fetched Categories:', categoriesData);
        setProducts(productsData);
        setCategories(categoriesData);

        // Favorileri yükle
        try {
          const favoritesData = await favoriteService.getFavorites();
          const favoriteIds = new Set<number>(favoritesData.map((f: { product_id: number }) => f.product_id));
          setFavorites(Array.from(favoriteIds));
        } catch (error) {
          console.error('Favoriler yüklenirken hata:', error);
        }

        loadTestDetails();
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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
      
      // Her detay için ürün bilgilerini al
      const detailsWithProducts = await Promise.all(
        response.data.sample_details.map(async (detail: ProductDetail) => {
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

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    try {
      console.log('Searching products by name:', query);
      // Her zaman tüm ürünleri al
      const allProducts = await productService.getAllProducts();
      console.log('All products:', allProducts);

      if (query.trim()) {
        // Frontend'de ürün isimlerine göre filtreleme yap
        const filteredProducts = allProducts.filter(product => 
          product.name.toLowerCase().includes(query.toLowerCase())
        );
        console.log('Filtered products:', filteredProducts);
        setProducts(filteredProducts);
      } else {
        setProducts(allProducts);
      }
    } catch (error) {
      console.error('Error searching products:', error);
      setProducts([]);
    }
  };

  const handleCategoryChange = async (categoryId: number | '') => {
    setSelectedCategory(categoryId);
    try {
      console.log('Filtering by category:', categoryId);
      // Her zaman tüm ürünleri al
      const allProducts = await productService.getAllProducts();
      console.log('All products:', allProducts);

      if (categoryId) {
        // Frontend'de kategoriye göre filtreleme yap
        const filteredProducts = allProducts.filter(product => 
          product.categories.some(category => category.id === categoryId)
        );
        console.log('Filtered products by category:', filteredProducts);
        setProducts(filteredProducts);
      } else {
        setProducts(allProducts);
      }
    } catch (error) {
      console.error('Error filtering by category:', error);
      setProducts([]);
    }
  };

  // Arama ve kategori filtrelemesini birlikte uygula
  const applyFilters = async () => {
    try {
      const allProducts = await productService.getAllProducts();
      console.log('All products:', allProducts);

      let filteredProducts = [...allProducts];

      // Kategori filtresini uygula
      if (selectedCategory) {
        filteredProducts = filteredProducts.filter(product => 
          product.categories.some(category => category.id === selectedCategory)
        );
      }

      // Arama filtresini uygula
      if (searchQuery.trim()) {
        filteredProducts = filteredProducts.filter(product => 
          product.name.toLowerCase().includes(searchQuery.toLowerCase())
        );
      }

      console.log('Filtered products:', filteredProducts);
      setProducts(filteredProducts);
    } catch (error) {
      console.error('Error applying filters:', error);
      setProducts([]);
    }
  };

  // Arama veya kategori değiştiğinde filtreleri uygula
  useEffect(() => {
    applyFilters();
  }, [searchQuery, selectedCategory]);

  const handleSort = (value: string) => {
    setSortBy(value);
    const sortedProducts = [...products].sort((a, b) => {
      const priceA = getLowestPrice(a.details || []);
      const priceB = getLowestPrice(b.details || []);
      
      switch (value) {
        case 'price_asc':
          if (priceA === null && priceB === null) return 0;
          if (priceA === null) return 1;
          if (priceB === null) return -1;
          return priceA - priceB;
        case 'price_desc':
          if (priceA === null && priceB === null) return 0;
          if (priceA === null) return 1;
          if (priceB === null) return -1;
          return priceB - priceA;
        case 'name':
        default:
          return a.name.localeCompare(b.name);
      }
    });
    setProducts(sortedProducts);
  };

  const getLowestPrice = (details: ProductDetail[]) => {
    if (!details || details.length === 0) return null;
    const validPrices = details.filter(d => d && d.price !== undefined && d.price !== null);
    if (validPrices.length === 0) return null;
    return Math.min(...validPrices.map(d => d.price));
  };

  const formatPrice = (price: number | null) => {
    if (price === null) return 'Fiyat bilgisi yok';
    return new Intl.NumberFormat('tr-TR', {
      style: 'currency',
      currency: 'TRY'
    }).format(price);
  };

  const handleProductClick = async (product: Product) => {
    try {
      console.log('Fetching product details for:', product.id);
      const productWithDetails = await productService.getProductById(product.id);
      console.log('Product details received:', productWithDetails);
      setSelectedProduct(productWithDetails);
      setOpenModal(true);
    } catch (error) {
      console.error('Error fetching product details:', error);
    }
  };

  const handleCloseModal = () => {
    setOpenModal(false);
    setSelectedProduct(null);
  };

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  const getMarketLogo = (market: Market | undefined) => {
    if (!market?.image_url) {
      return (
        <Box
          sx={{
            width: 24,
            height: 24,
            borderRadius: '50%',
            bgcolor: 'primary.main',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '0.75rem',
            fontWeight: 'bold',
          }}
        >
          {market?.name?.charAt(0) || '?'}
        </Box>
      );
    }
    return (
      <img
        src={market.image_url}
        alt={market.name}
        style={{ width: 24, height: 24, objectFit: 'contain' }}
      />
    );
  };

  const handleToggleFavorite = async (productId: number) => {
    try {
      const isFavorite = favorites.includes(productId);
      const method = isFavorite ? 'DELETE' : 'POST';
      await axios({
        method,
        url: `http://localhost:8000/api/v1/favorites/${productId}`
      });

      setFavorites(prev =>
        isFavorite
          ? prev.filter(id => id !== productId)
          : [...prev, productId]
      );

      setSnackbar({
        open: true,
        message: isFavorite ? 'Ürün favorilerden çıkarıldı' : 'Ürün favorilere eklendi',
        severity: 'success'
      });
    } catch (err) {
      console.error('Error toggling favorite:', err);
      setSnackbar({
        open: true,
        message: 'Favori işlemi sırasında bir hata oluştu',
        severity: 'error'
      });
    }
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
            Market Fiyat Karşılaştırma
          </Typography>
          <Button
            color="inherit"
            startIcon={<Logout />}
            onClick={handleLogout}
          >
            Çıkış Yap
          </Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ py: 2 }}>
        <Box sx={{ mb: 4 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Ürün Ara"
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Kategori</InputLabel>
                <Select
                  value={selectedCategory}
                  label="Kategori"
                  onChange={(e) => handleCategoryChange(e.target.value as number | '')}
                >
                  <MenuItem value="">Tümü</MenuItem>
                  {categories.map((category) => (
                    <MenuItem key={category.id} value={category.id}>
                      {category.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Sırala</InputLabel>
                <Select
                  value={sortBy}
                  label="Sırala"
                  onChange={(e) => handleSort(e.target.value)}
                >
                  <MenuItem value="name">İsme Göre</MenuItem>
                  <MenuItem value="price_asc">Fiyat (Düşükten Yükseğe)</MenuItem>
                  <MenuItem value="price_desc">Fiyat (Yüksekten Düşüğe)</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Box>

        {products.length === 0 ? (
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <Typography variant="h6" color="text.secondary">
              Ürün bulunamadı
            </Typography>
          </Box>
        ) : (
          <Grid container spacing={3}>
            {products.map((product) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={product.id}>
                <Card
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    position: 'relative',
                    '&:hover': {
                      boxShadow: 6,
                      cursor: 'pointer'
                    }
                  }}
                  onClick={() => handleProductClick(product)}
                >
                  <CardMedia
                    component="img"
                    height="200"
                    image={product.image_url || 'https://via.placeholder.com/200'}
                    alt={product.name}
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="h2">
                      {product.name}
                    </Typography>
                    {product.brand && (
                      <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
                        {product.brand}
                      </Typography>
                    )}
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {product.description}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="h6" color="primary">
                        {formatPrice(getLowestPrice(product.details || []))}
                      </Typography>
                      <Box>
                        <IconButton
                          sx={{
                            bgcolor: 'background.paper',
                            '&:hover': {
                              bgcolor: 'action.hover'
                            }
                          }}
                          onClick={(e) => {
                            e.stopPropagation();
                            handleToggleFavorite(product.id);
                          }}
                        >
                          {favorites.includes(product.id) ? (
                            <Favorite color="error" />
                          ) : (
                            <FavoriteBorder />
                          )}
                        </IconButton>
                        <IconButton
                          onClick={(e: React.MouseEvent) => {
                            e.stopPropagation();
                            // Fiyat karşılaştırma işlemi
                          }}
                        >
                          <CompareArrows />
                        </IconButton>
                      </Box>
                    </Box>
                  </CardContent>
                  <Box sx={{ position: 'absolute', top: 8, right: 8 }}>
                    <IconButton
                      sx={{
                        bgcolor: 'background.paper',
                        '&:hover': {
                          bgcolor: 'action.hover'
                        }
                      }}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleToggleFavorite(product.id);
                      }}
                    >
                      {favorites.includes(product.id) ? (
                        <Favorite color="error" />
                      ) : (
                        <FavoriteBorder />
                      )}
                    </IconButton>
                  </Box>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Container>

      {/* Product Detail Modal */}
      <Modal
        open={openModal}
        onClose={handleCloseModal}
        aria-labelledby="product-detail-modal"
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Box sx={{
          position: 'relative',
          width: '80%',
          maxWidth: 800,
          bgcolor: 'background.paper',
          borderRadius: 2,
          boxShadow: 24,
          p: 4,
          maxHeight: '90vh',
          overflow: 'auto',
        }}>
          <IconButton
            onClick={handleCloseModal}
            sx={{
              position: 'absolute',
              right: 8,
              top: 8,
            }}
          >
            <Close />
          </IconButton>

          {selectedProduct && (
            <>
              {/* Ürün Detayları */}
              <Box sx={{ mb: 4 }}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={4}>
                    <CardMedia
                      component="img"
                      image={selectedProduct.image_url || 'https://via.placeholder.com/300'}
                      alt={selectedProduct.name}
                      sx={{ width: '100%', borderRadius: 8 }}
                    />
                  </Grid>
                  <Grid item xs={12} md={8}>
                    <Typography variant="h4" gutterBottom>
                      {selectedProduct.name}
                    </Typography>
                    {selectedProduct.brand && (
                      <Typography variant="h6" color="text.secondary" gutterBottom>
                        {selectedProduct.brand}
                      </Typography>
                    )}
                    <Typography variant="body1" paragraph>
                      {selectedProduct.description}
                    </Typography>
                    <Typography variant="h5" color="primary" gutterBottom>
                      En Düşük Fiyat: {formatPrice(getLowestPrice(selectedProduct.details || []))}
                    </Typography>
                  </Grid>
                </Grid>
              </Box>

              {/* Market Fiyatları Tablosu */}
              <Typography variant="h6" gutterBottom>
                Market Fiyatları
              </Typography>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Market</TableCell>
                      <TableCell>Fiyat</TableCell>
                      <TableCell>Son Güncelleme</TableCell>
                      <TableCell>Durum</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {selectedProduct.details && selectedProduct.details.length > 0 ? (
                      selectedProduct.details
                        .sort((a, b) => (a.price || 0) - (b.price || 0))
                        .map((detail) => (
                          <TableRow 
                            key={detail.id}
                            sx={{
                              backgroundColor: detail.price === getLowestPrice(selectedProduct.details || []) 
                                ? 'rgba(25, 118, 210, 0.08)' 
                                : 'inherit'
                            }}
                          >
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                {getMarketLogo(detail.market as Market)}
                                {detail.market?.name || 'Bilinmeyen Market'}
                              </Box>
                            </TableCell>
                            <TableCell>
                              {formatPrice(detail.price)}
                            </TableCell>
                            <TableCell>
                              {detail.updated_at ? new Date(detail.updated_at).toLocaleDateString('tr-TR') : 'Bilinmiyor'}
                            </TableCell>
                            <TableCell>
                              {detail.price === getLowestPrice(selectedProduct.details || []) ? (
                                <Typography color="primary" fontWeight="bold">
                                  En Uygun Fiyat
                                </Typography>
                              ) : (
                                <Typography color="text.secondary">
                                  {((detail.price || 0) - (getLowestPrice(selectedProduct.details || []) || 0)).toLocaleString('tr-TR', {
                                    style: 'currency',
                                    currency: 'TRY',
                                  })} fark
                                </Typography>
                              )}
                            </TableCell>
                          </TableRow>
                        ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={4} align="center">
                          Bu ürün için fiyat bilgisi bulunmamaktadır.
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>

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
                  onClick={() => {
                    if (selectedProduct && selectedProduct.details && selectedProduct.details.length > 0) {
                      handleToggleFavorite(selectedProduct.details[0].id);
                    }
                  }}
                >
                  {selectedProduct && selectedProduct.details && selectedProduct.details.length > 0 && favorites.includes(selectedProduct.id) ? (
                    <Favorite color="error" />
                  ) : (
                    <FavoriteBorder />
                  )}
                </Button>
              </Box>
            </>
          )}
        </Box>
      </Modal>
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

export default Home; 

/*                   */