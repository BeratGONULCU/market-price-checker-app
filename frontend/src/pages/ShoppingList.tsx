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
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Divider,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  Snackbar,
  Tabs,
  Tab,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Save as SaveIcon,
  Print as PrintIcon,
  Share as ShareIcon,
  Category as CategoryIcon,
  LocalOffer as LocalOfferIcon,
  ShoppingCart as ShoppingCartIcon,
  FileDownload as FileDownloadIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Product } from '../types/product';
import { Market } from '../types/market';
import { useSnackbar } from 'notistack';
import shoppingListService from '../services/shoppingList';
import { ShoppingList, ShoppingListItem } from '../types';

interface MarketComparison {
  market_id: number;
  market_name: string;
  total_price: number;
  items: {
    product_id: number;
    product_name: string;
    price: number;
    quantity: number;
  }[];
}

const ShoppingListPage: React.FC = () => {
  const navigate = useNavigate();
  const [lists, setLists] = useState<ShoppingList[]>([]);
  const [selectedList, setSelectedList] = useState<ShoppingList | null>(null);
  const [loading, setLoading] = useState(true);
  const [showNewListDialog, setShowNewListDialog] = useState(false);
  const [newListName, setNewListName] = useState('');
  const [activeTab, setActiveTab] = useState(0);
  const [marketComparisons, setMarketComparisons] = useState<MarketComparison[]>([]);
  const { enqueueSnackbar } = useSnackbar();
  const [showAddItemDialog, setShowAddItemDialog] = useState(false);
  const [newItem, setNewItem] = useState({ product_id: 0, quantity: 1 });
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetchLists();
  }, []);

  useEffect(() => {
    if (selectedList) {
      loadMarketComparisons();
    }
  }, [selectedList]);

  useEffect(() => {
    loadProducts();
  }, []);

  const fetchLists = async () => {
    try {
      setLoading(true);
      const data = await shoppingListService.getLists();
      setLists(data);
    } catch (error) {
      console.error('Error fetching shopping lists:', error);
      enqueueSnackbar('Alışveriş listeleri yüklenirken bir hata oluştu', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const loadMarketComparisons = async () => {
    if (!selectedList) return;

    try {
      const response = await axios.get(`http://localhost:8000/api/v1/shopping-lists/${selectedList.id}/market-comparison`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      setMarketComparisons(response.data);
    } catch (error) {
      console.error('Market karşılaştırması yüklenirken hata:', error);
    }
  };

  const loadProducts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/products', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      setProducts(response.data);
    } catch (error) {
      console.error('Ürünler yüklenirken hata:', error);
      enqueueSnackbar('Ürünler yüklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleCreateList = async () => {
    if (!newListName.trim()) {
      enqueueSnackbar('Liste adı boş olamaz', { variant: 'error' });
      return;
    }

    try {
      const newList = await shoppingListService.createList(newListName);
      setLists(prev => [...prev, newList]);
      setNewListName('');
      setShowNewListDialog(false);
      enqueueSnackbar('Alışveriş listesi oluşturuldu', { variant: 'success' });
    } catch (error) {
      console.error('Error creating shopping list:', error);
      enqueueSnackbar('Alışveriş listesi oluşturulurken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleDeleteList = async (listId: number) => {
    try {
      await shoppingListService.deleteList(listId);
      setLists(prev => prev.filter(list => list.id !== listId));
      enqueueSnackbar('Alışveriş listesi silindi', { variant: 'success' });
    } catch (error) {
      console.error('Error deleting shopping list:', error);
      enqueueSnackbar('Alışveriş listesi silinirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleEditClick = (list: ShoppingList) => {
    setSelectedList(list);
    setNewListName(list.name);
    setShowNewListDialog(true);
  };

  const handleUpdateList = async () => {
    if (!selectedList || !newListName.trim()) {
      enqueueSnackbar('Liste adı boş olamaz', { variant: 'error' });
      return;
    }

    try {
      const updatedList = await shoppingListService.updateList(selectedList.id, newListName);
      setLists(prev => prev.map(list => list.id === updatedList.id ? updatedList : list));
      setNewListName('');
      setSelectedList(null);
      setShowNewListDialog(false);
      enqueueSnackbar('Alışveriş listesi güncellendi', { variant: 'success' });
    } catch (error) {
      console.error('Error updating shopping list:', error);
      enqueueSnackbar('Alışveriş listesi güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleDeleteItem = async (itemId: number) => {
    try {
      await axios.delete(`http://localhost:8000/api/v1/shopping-lists/items/${itemId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (selectedList) {
        const updatedItems = selectedList.items.filter(item => item.id !== itemId);
        setSelectedList({ ...selectedList, items: updatedItems });
        enqueueSnackbar('Ürün listeden kaldırıldı', { variant: 'success' });
      }
    } catch (error) {
      console.error('Ürün silinirken hata:', error);
      enqueueSnackbar('Ürün silinirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleToggleItem = async (itemId: number) => {
    try {
      const item = selectedList?.items.find(i => i.id === itemId);
      if (!item) return;

      await axios.put(`http://localhost:8000/api/v1/shopping-lists/items/${itemId}`, {
        is_checked: !item.is_checked
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (selectedList) {
        const updatedItems = selectedList.items.map(item =>
          item.id === itemId ? { ...item, is_checked: !item.is_checked } : item
        );
        setSelectedList({ ...selectedList, items: updatedItems });
      }
    } catch (error) {
      console.error('Ürün durumu güncellenirken hata:', error);
      enqueueSnackbar('Ürün durumu güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handlePrintList = () => {
    window.print();
  };

  const handleShareList = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/api/v1/shopping-lists/${selectedList?.id}/share`, {}, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      navigator.clipboard.writeText(response.data.share_url);
      enqueueSnackbar('Paylaşım linki kopyalandı', { variant: 'success' });
    } catch (error) {
      console.error('Liste paylaşılırken hata:', error);
      enqueueSnackbar('Liste paylaşılırken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleExportPDF = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/shopping-lists/${selectedList?.id}/export`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${selectedList?.name}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      enqueueSnackbar('PDF dosyası indirildi', { variant: 'success' });
    } catch (error) {
      console.error('PDF indirilirken hata:', error);
      enqueueSnackbar('PDF indirilirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleAddItem = async () => {
    if (!selectedList) return;

    try {
      const response = await axios.post(
        `http://localhost:8000/api/v1/shopping-lists/${selectedList.id}/items`,
        newItem,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );

      // Listeyi güncelle
      const updatedList = { ...selectedList };
      updatedList.items = [...updatedList.items, response.data];
      setSelectedList(updatedList);

      setShowAddItemDialog(false);
      setNewItem({ product_id: 0, quantity: 1 });
      enqueueSnackbar('Ürün listeye eklendi', { variant: 'success' });
    } catch (error) {
      console.error('Ürün eklenirken hata:', error);
      enqueueSnackbar('Ürün eklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Alışveriş Listeleri
          </Typography>
          <Button
            color="inherit"
            startIcon={<AddIcon />}
            onClick={() => {
              setSelectedList(null);
              setNewListName('');
              setShowNewListDialog(true);
            }}
          >
            Yeni Liste
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Grid container spacing={3}>
          {/* Liste Seçimi */}
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Listelerim
                </Typography>
                <List>
                  {lists.map((list) => (
                    <ListItem
                      key={list.id}
                      button
                      selected={selectedList?.id === list.id}
                      onClick={() => {
                        setSelectedList(list);
                        setNewListName(list.name);
                        setShowNewListDialog(true);
                      }}
                    >
                      <ListItemText
                        primary={list.name}
                        secondary={`${list.items.length} ürün`}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Seçili Liste İçeriği */}
          <Grid item xs={12} md={9}>
            {selectedList ? (
              <Card>
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h5">
                      {selectedList.name}
                    </Typography>
                    <Box>
                      <IconButton onClick={handlePrintList}>
                        <PrintIcon />
                      </IconButton>
                      <IconButton onClick={handleShareList}>
                        <ShareIcon />
                      </IconButton>
                      <IconButton onClick={handleExportPDF}>
                        <FileDownloadIcon />
                      </IconButton>
                    </Box>
                  </Box>

                  <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} sx={{ mb: 2 }}>
                    <Tab icon={<ShoppingCartIcon />} label="Ürünler" />
                    <Tab icon={<CategoryIcon />} label="Kategoriler" />
                    <Tab icon={<LocalOfferIcon />} label="Market Karşılaştırması" />
                  </Tabs>

                  {activeTab === 0 && (
                    <>
                      <Box display="flex" justifyContent="flex-end" mb={2}>
                        <Button
                          variant="contained"
                          startIcon={<AddIcon />}
                          onClick={() => setShowAddItemDialog(true)}
                        >
                          Ürün Ekle
                        </Button>
                      </Box>
                      <List>
                        {selectedList.items.map((item) => (
                          <React.Fragment key={item.id}>
                            <ListItem>
                              <ListItemText
                                primary={item.product.name}
                                secondary={`${item.quantity} adet - ${item.product.details[0]?.price.toLocaleString('tr-TR', {
                                  style: 'currency',
                                  currency: 'TRY'
                                })}`}
                              />
                              <ListItemSecondaryAction>
                                <IconButton
                                  edge="end"
                                  onClick={() => handleToggleItem(item.id)}
                                  color={item.is_checked ? 'primary' : 'default'}
                                >
                                  <SaveIcon />
                                </IconButton>
                                <IconButton
                                  edge="end"
                                  onClick={() => handleDeleteItem(item.id)}
                                >
                                  <DeleteIcon />
                                </IconButton>
                              </ListItemSecondaryAction>
                            </ListItem>
                            <Divider />
                          </React.Fragment>
                        ))}
                        {selectedList.items.length === 0 && (
                          <Typography variant="body1" color="text.secondary" align="center" sx={{ py: 4 }}>
                            Bu listede henüz ürün yok
                          </Typography>
                        )}
                      </List>
                    </>
                  )}

                  {activeTab === 1 && (
                    <Box>
                      {/* Kategorilere göre gruplandırılmış ürünler */}
                      {Object.entries(
                        selectedList.items.reduce((acc, item) => {
                          const category = item.product.category.name;
                          if (!acc[category]) {
                            acc[category] = [];
                          }
                          acc[category].push(item);
                          return acc;
                        }, {} as Record<string, typeof selectedList.items>)
                      ).map(([categoryId, items]) => (
                        <Box key={categoryId} sx={{ mb: 3 }}>
                          <Typography variant="h6" gutterBottom>
                            {categoryId}
                          </Typography>
                          <List>
                            {items.map((item) => (
                              <React.Fragment key={item.id}>
                                <ListItem>
                                  <ListItemText
                                    primary={item.product.name}
                                    secondary={`${item.quantity} adet`}
                                  />
                                  <ListItemSecondaryAction>
                                    <IconButton
                                      edge="end"
                                      onClick={() => handleToggleItem(item.id)}
                                      color={item.is_checked ? 'primary' : 'default'}
                                    >
                                      <SaveIcon />
                                    </IconButton>
                                    <IconButton
                                      edge="end"
                                      onClick={() => handleDeleteItem(item.id)}
                                    >
                                      <DeleteIcon />
                                    </IconButton>
                                  </ListItemSecondaryAction>
                                </ListItem>
                                <Divider />
                              </React.Fragment>
                            ))}
                          </List>
                        </Box>
                      ))}
                    </Box>
                  )}

                  {activeTab === 2 && (
                    <Box>
                      <TableContainer component={Paper}>
                        <Table>
                          <TableHead>
                            <TableRow>
                              <TableCell>Market</TableCell>
                              <TableCell align="right">Toplam Fiyat</TableCell>
                              <TableCell align="right">Tasarruf</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {marketComparisons.map((comparison) => (
                              <TableRow key={comparison.market_id}>
                                <TableCell>{comparison.market_name}</TableCell>
                                <TableCell align="right">
                                  {comparison.total_price.toLocaleString('tr-TR', {
                                    style: 'currency',
                                    currency: 'TRY'
                                  })}
                                </TableCell>
                                <TableCell align="right">
                                  {((marketComparisons[0]?.total_price || 0) - comparison.total_price).toLocaleString('tr-TR', {
                                    style: 'currency',
                                    currency: 'TRY'
                                  })}
                                </TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableContainer>

                      {marketComparisons.map((comparison) => (
                        <Box key={comparison.market_id} sx={{ mt: 3 }}>
                          <Typography variant="h6" gutterBottom>
                            {comparison.market_name} - Ürün Listesi
                          </Typography>
                          <TableContainer component={Paper}>
                            <Table>
                              <TableHead>
                                <TableRow>
                                  <TableCell>Ürün</TableCell>
                                  <TableCell align="right">Adet</TableCell>
                                  <TableCell align="right">Birim Fiyat</TableCell>
                                  <TableCell align="right">Toplam</TableCell>
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                {comparison.items.map((item) => (
                                  <TableRow key={item.product_id}>
                                    <TableCell>{item.product_name}</TableCell>
                                    <TableCell align="right">{item.quantity}</TableCell>
                                    <TableCell align="right">
                                      {item.price.toLocaleString('tr-TR', {
                                        style: 'currency',
                                        currency: 'TRY'
                                      })}
                                    </TableCell>
                                    <TableCell align="right">
                                      {(item.price * item.quantity).toLocaleString('tr-TR', {
                                        style: 'currency',
                                        currency: 'TRY'
                                      })}
                                    </TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          </TableContainer>
                        </Box>
                      ))}
                    </Box>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardContent>
                  <Typography variant="body1" color="text.secondary" align="center">
                    Lütfen bir liste seçin veya yeni liste oluşturun
                  </Typography>
                </CardContent>
              </Card>
            )}
          </Grid>
        </Grid>
      </Container>

      {/* Yeni Liste Dialog'u */}
      <Dialog open={showNewListDialog} onClose={() => setShowNewListDialog(false)}>
        <DialogTitle>
          {selectedList ? 'Listeyi Düzenle' : 'Yeni Alışveriş Listesi'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Liste Adı"
            fullWidth
            value={newListName}
            onChange={(e) => setNewListName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowNewListDialog(false)}>İptal</Button>
          <Button
            onClick={selectedList ? handleUpdateList : handleCreateList}
            color="primary"
          >
            {selectedList ? 'Güncelle' : 'Oluştur'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Ürün Ekleme Dialog'u */}
      <Dialog open={showAddItemDialog} onClose={() => setShowAddItemDialog(false)}>
        <DialogTitle>Ürün Ekle</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>Ürün</InputLabel>
            <Select
              value={newItem.product_id}
              onChange={(e) => setNewItem({ ...newItem, product_id: Number(e.target.value) })}
              label="Ürün"
            >
              {products.map((product) => (
                <MenuItem key={product.id} value={product.id}>
                  {product.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            fullWidth
            type="number"
            label="Adet"
            value={newItem.quantity}
            onChange={(e) => setNewItem({ ...newItem, quantity: Number(e.target.value) })}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAddItemDialog(false)}>İptal</Button>
          <Button onClick={handleAddItem} variant="contained">
            Ekle
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default ShoppingListPage; 