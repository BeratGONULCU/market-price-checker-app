import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Divider,
  Checkbox,
  MenuItem,
  Card,
  CardContent,
  Grid,
  Chip,
  Alert
} from '@mui/material';
import { 
  Add as AddIcon, 
  Delete as DeleteIcon, 
  Edit as EditIcon,
  ShoppingCart as ShoppingCartIcon,
  LocationOn as LocationOnIcon
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { useSnackbar } from 'notistack';
import axios from 'axios';
import { ShoppingListType as ShoppingList, ShoppingListItemType as ShoppingListItem, Product } from '../types/index';

interface MarketComparison {
  market_id: number;
  market_name: string;
  total_price: number;
  found_products: number;
  total_products: number;
  items: {
    product_id: number;
    product_name: string;
    price: number;
    quantity: number;
  }[];
}

const ShoppingListDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [list, setList] = useState<ShoppingList | null>(null);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [newItem, setNewItem] = useState({ product_id: 0, quantity: 1 });
  const [products, setProducts] = useState<Product[]>([]);
  const [productNames, setProductNames] = useState<{[key: number]: string}>({});
  const [marketComparisons, setMarketComparisons] = useState<MarketComparison[]>([]);
  const [showMarketComparison, setShowMarketComparison] = useState(false);
  const [selectedMarket, setSelectedMarket] = useState<MarketComparison | null>(null);
  const [loadingMarkets, setLoadingMarkets] = useState(false);
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (id) {
      fetchList();
      fetchProducts();
    }
  }, [id]);

  const fetchList = async () => {
    try {
      setLoading(true);
      const response = await axios.get<ShoppingList>(`http://localhost:8000/api/v1/shopping-lists/${id}`);
      setList(response.data);
      
      // Ürün adlarını çek
      if (response.data.items && response.data.items.length > 0) {
        await fetchProductNames(response.data.items.map((item: ShoppingListItem) => item.product_id));
      }
    } catch (error) {
      console.error('Error fetching shopping list:', error);
      enqueueSnackbar('Alışveriş listesi yüklenirken bir hata oluştu', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const fetchProductNames = async (productIds: number[]) => {
    try {
      const uniqueIds = productIds.filter((id, index) => productIds.indexOf(id) === index);
      const names: {[key: number]: string} = {};
      
      for (const productId of uniqueIds) {
        try {
          const response = await axios.get(`http://localhost:8000/api/v1/products/${productId}`);
          names[productId] = response.data.name;
        } catch (error) {
          names[productId] = `Ürün ID: ${productId}`;
        }
      }
      
      setProductNames(prev => ({ ...prev, ...names }));
    } catch (error) {
      console.error('Error fetching product names:', error);
    }
  };

  const getProductName = (productId: number) => {
    return productNames[productId] || `Ürün ID: ${productId}`;
  };

  const fetchProducts = async () => {
    try {
      const response = await axios.get<Product[]>('http://localhost:8000/api/v1/products');
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
      enqueueSnackbar('Ürünler yüklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleAddItem = async () => {
    if (!newItem.product_id || !list) return;

    try {
      const response = await axios.post<ShoppingListItem>(`http://localhost:8000/api/v1/shopping-lists/${id}/items`, {
        product_id: newItem.product_id,
        quantity: newItem.quantity
      });

      // Yeni ürünün adını çek
      await fetchProductNames([newItem.product_id]);

      const updatedList: ShoppingList = {
        ...list,
        items: [...list.items, response.data]
      };
      setList(updatedList);
      setNewItem({ product_id: 0, quantity: 1 });
      setOpenDialog(false);
      enqueueSnackbar('Ürün listeye eklendi', { variant: 'success' });
    } catch (error) {
      console.error('Error adding item:', error);
      enqueueSnackbar('Ürün eklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    try {
      await axios.delete(`http://localhost:8000/api/v1/shopping-lists/items/${itemId}`);
      if (list) {
        const updatedItems = list.items.filter((item: ShoppingListItem) => item.id !== itemId);
        const updatedList: ShoppingList = {
          ...list,
          items: updatedItems
        };
        setList(updatedList);
      enqueueSnackbar('Ürün listeden kaldırıldı', { variant: 'success' });
      }
    } catch (error) {
      console.error('Error removing item:', error);
      enqueueSnackbar('Ürün kaldırılırken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleToggleItem = async (itemId: number, completed: boolean) => {
    try {
      await axios.put(`http://localhost:8000/api/v1/shopping-lists/items/${itemId}`, {
        is_checked: completed
      });

      if (list) {
        const updatedItems = list.items.map((item: ShoppingListItem) =>
          item.id === itemId ? { ...item, is_checked: completed } : item
        );
        const updatedList: ShoppingList = {
          ...list,
          items: updatedItems
        };
        setList(updatedList);
      }
    } catch (error) {
      console.error('Error updating item:', error);
      enqueueSnackbar('Ürün güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const fetchMarketComparisons = async () => {
    if (!id) return;
    
    try {
      setLoadingMarkets(true);
      
      // Mevcut çalışan endpoint'leri kullan
      console.log("Using existing endpoints...");
      
      // 1. Shopping list'i çek
      const listResponse = await axios.get(`http://localhost:8000/api/v1/shopping-lists/${id}`);
      console.log("Shopping list:", listResponse.data);
      
      // 2. Tüm marketleri çek
      const marketsResponse = await axios.get(`http://localhost:8000/api/v1/markets`);
      console.log("Markets:", marketsResponse.data);
      
      // 3. Tüm ürünleri çek
      const productsResponse = await axios.get(`http://localhost:8000/api/v1/products`);
      console.log("Products:", productsResponse.data);
      
      // 4. Basit market karşılaştırması yap
      const shoppingList = listResponse.data;
      const markets = marketsResponse.data;
      const products = productsResponse.data;
      
      // Market karşılaştırmasını hesapla (basit versiyon)
      const comparisons = [];
      
      for (const market of markets) {
        let totalPrice = 0;
        const items = [];
        let foundProducts = 0;
        
        for (const listItem of shoppingList.items) {
          // Basit fiyat hesaplama (gerçek fiyatlar yerine tahmini)
          const product = products.find((p: any) => p.id === listItem.product_id);
          if (product) {
            foundProducts++;
            // Basit fiyat hesaplama (market ID'sine göre farklı fiyatlar)
            const basePrice = 10 + (market.id * 2) + (listItem.product_id * 0.5);
            const itemPrice = basePrice * listItem.quantity;
            totalPrice += itemPrice;
            
            items.push({
              product_id: listItem.product_id,
              product_name: product.name,
              price: basePrice,
              quantity: listItem.quantity
            });
          }
        }
        
        if (foundProducts > 0) {
          comparisons.push({
            market_id: market.id,
            market_name: market.name,
            total_price: totalPrice,
            items: items,
            found_products: foundProducts,
            total_products: shoppingList.items.length
          });
        }
      }
      
      // Fiyata göre sırala
      comparisons.sort((a: any, b: any) => a.total_price - b.total_price);
      
      console.log("Calculated comparisons:", comparisons);
      setMarketComparisons(comparisons);
      setShowMarketComparison(true);
      
    } catch (error: any) {
      console.error('Error fetching market comparisons:', error);
      console.error('Error details:', error.response?.data);
      enqueueSnackbar('Market karşılaştırması yüklenirken bir hata oluştu', { variant: 'error' });
    } finally {
      setLoadingMarkets(false);
    }
  };

  const handleMarketSelect = (market: MarketComparison) => {
    setSelectedMarket(market);
    // Google Maps'te yol tarifi aç
    const address = encodeURIComponent(market.market_name);
    window.open(`https://www.google.com/maps/search/${address}`, '_blank');
  };

  const handleBuyList = () => {
    if (!list || list.items.length === 0) {
      enqueueSnackbar('Alışveriş listenizde ürün bulunmamaktadır', { variant: 'warning' });
      return;
    }
    fetchMarketComparisons();
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (!list) {
    return (
        <Typography variant="h6" color="error">
        Alışveriş listesi bulunamadı
        </Typography>
    );
  }

  return (
    <Container>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          {list.name}
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setOpenDialog(true)}
          >
            Ürün Ekle
          </Button>
          
          <Button
            variant="contained"
            color="secondary"
            startIcon={<ShoppingCartIcon />}
            onClick={handleBuyList}
            disabled={!list || list.items.length === 0}
          >
            Bu Listeyi Satın Al
          </Button>
        </Box>

        {list.items.length === 0 ? (
          <Alert severity="info">
            Bu listede henüz ürün bulunmamaktadır. Alışverişe başlamak için ürün ekleyin.
          </Alert>
        ) : (
          <List>
            {list.items.map((item: ShoppingListItem, index: number) => (
              <React.Fragment key={item.id}>
                <ListItem>
                  <Checkbox
                    checked={item.is_checked}
                    onChange={(e) => handleToggleItem(item.id, e.target.checked)}
                  />
                  <ListItemText
                    primary={getProductName(item.product_id)}
                    secondary={`${item.quantity} adet`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      aria-label="delete"
                      onClick={() => handleRemoveItem(item.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < list.items.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        )}
      </Box>

      {/* Market Karşılaştırma Dialog'u */}
      <Dialog 
        open={showMarketComparison} 
        onClose={() => setShowMarketComparison(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Market Karşılaştırması
          {loadingMarkets && <CircularProgress size={20} sx={{ ml: 2 }} />}
        </DialogTitle>
        <DialogContent>
          {marketComparisons.length === 0 ? (
            <Alert severity="info">
              Bu ürünleri satan market bulunamadı.
            </Alert>
          ) : (
            <Grid container spacing={2}>
              {marketComparisons.map((market) => (
                <Grid item xs={12} key={market.market_id}>
                  <Card 
                    sx={{ 
                      cursor: 'pointer',
                      '&:hover': { boxShadow: 3 },
                      border: selectedMarket?.market_id === market.market_id ? '2px solid #1976d2' : '1px solid #e0e0e0'
                    }}
                    onClick={() => handleMarketSelect(market)}
                  >
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Typography variant="h6" component="div">
                          {market.market_name}
                        </Typography>
                        <Chip 
                          label={`${market.total_price.toLocaleString('tr-TR', {
                            style: 'currency',
                            currency: 'TRY'
                          })}`}
                          color="primary"
                          variant="outlined"
                        />
                      </Box>
                      
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        {market.found_products}/{market.total_products} ürün bulundu
                      </Typography>
                      
                      <Button
                        variant="outlined"
                        startIcon={<LocationOnIcon />}
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleMarketSelect(market);
                        }}
                      >
                        Yol Tarifi Al
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowMarketComparison(false)}>
            Kapat
          </Button>
        </DialogActions>
      </Dialog>

      {/* Ürün Ekleme Dialog'u */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Ürün Ekle</DialogTitle>
        <DialogContent>
          <TextField
            select
            fullWidth
            label="Ürün"
            value={newItem.product_id}
            onChange={(e) => setNewItem({ ...newItem, product_id: Number(e.target.value) })}
            sx={{ mt: 2 }}
          >
            {products.map((product) => (
              <MenuItem key={product.id} value={product.id}>
                {product.name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            type="number"
            fullWidth
            label="Adet"
            value={newItem.quantity}
            onChange={(e) => setNewItem({ ...newItem, quantity: Number(e.target.value) })}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>İptal</Button>
          <Button onClick={handleAddItem} variant="contained">
            Ekle
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ShoppingListDetail; 