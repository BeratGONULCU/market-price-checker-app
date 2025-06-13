import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Box,
  Paper,
  Grid,
  Card,
  CardMedia,
  CardContent
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon, ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { useSnackbar } from 'notistack';
import { useAuth } from '../contexts/AuthContext';
import shoppingListService from '../services/shoppingList';
import { ShoppingList, ShoppingListItem } from '../types/shoppingList';

const ShoppingListDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { enqueueSnackbar } = useSnackbar();
  const [list, setList] = useState<ShoppingList | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingItem, setEditingItem] = useState<ShoppingListItem | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [notes, setNotes] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    if (id) {
      loadList();
    }
  }, [user, navigate, id]);

  const loadList = async () => {
    if (!id) return;
    try {
      const data = await shoppingListService.getShoppingList(parseInt(id));
      setList(data);
    } catch (error) {
      enqueueSnackbar('Alışveriş listesi yüklenirken bir hata oluştu', { variant: 'error' });
      navigate('/shopping-lists');
    }
  };

  const handleAddItem = async () => {
    if (!list) return;
    try {
      await shoppingListService.addItemToList(list.id, 0, quantity, notes); // product_id 0 olarak gönderiliyor, bu kısmı daha sonra düzelteceğiz
      enqueueSnackbar('Ürün listeye eklendi', { variant: 'success' });
      setOpenDialog(false);
      setQuantity(1);
      setNotes('');
      loadList();
    } catch (error) {
      enqueueSnackbar('Ürün listeye eklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleUpdateItem = async () => {
    if (!editingItem) return;
    try {
      await shoppingListService.updateListItem(editingItem.id, quantity, notes);
      enqueueSnackbar('Ürün güncellendi', { variant: 'success' });
      setOpenDialog(false);
      setQuantity(1);
      setNotes('');
      setEditingItem(null);
      loadList();
    } catch (error) {
      enqueueSnackbar('Ürün güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleDeleteItem = async (itemId: number) => {
    if (!window.confirm('Bu ürünü listeden silmek istediğinizden emin misiniz?')) return;
    try {
      await shoppingListService.deleteListItem(itemId);
      enqueueSnackbar('Ürün listeden silindi', { variant: 'success' });
      loadList();
    } catch (error) {
      enqueueSnackbar('Ürün silinirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleOpenDialog = (item?: ShoppingListItem) => {
    if (item) {
      setEditingItem(item);
      setQuantity(item.quantity);
      setNotes(item.notes || '');
    } else {
      setEditingItem(null);
      setQuantity(1);
      setNotes('');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setQuantity(1);
    setNotes('');
    setEditingItem(null);
  };

  if (!list) {
    return null;
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Box display="flex" alignItems="center" mb={3}>
        <IconButton onClick={() => navigate('/shopping-lists')} sx={{ mr: 2 }}>
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h4" component="h1">
          {list.name}
        </Typography>
      </Box>

      <Box display="flex" justifyContent="flex-end" mb={3}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Ürün Ekle
        </Button>
      </Box>

      <Grid container spacing={2}>
        {list.items.map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item.id}>
            <Card>
              {item.product?.image_url && (
                <CardMedia
                  component="img"
                  height="140"
                  image={item.product.image_url}
                  alt={item.product.name}
                />
              )}
              <CardContent>
                <Typography variant="h6" component="h2">
                  {item.product?.name || 'Ürün'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Miktar: {item.quantity}
                </Typography>
                {item.notes && (
                  <Typography variant="body2" color="text.secondary">
                    Not: {item.notes}
                  </Typography>
                )}
              </CardContent>
              <Box display="flex" justifyContent="flex-end" p={1}>
                <IconButton
                  size="small"
                  onClick={() => handleOpenDialog(item)}
                >
                  <EditIcon />
                </IconButton>
                <IconButton
                  size="small"
                  onClick={() => handleDeleteItem(item.id)}
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>
          {editingItem ? 'Ürünü Düzenle' : 'Ürün Ekle'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Miktar"
            type="number"
            fullWidth
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value))}
            inputProps={{ min: 1 }}
          />
          <TextField
            margin="dense"
            label="Notlar"
            type="text"
            fullWidth
            multiline
            rows={2}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>İptal</Button>
          <Button
            onClick={editingItem ? handleUpdateItem : handleAddItem}
            color="primary"
            disabled={quantity < 1}
          >
            {editingItem ? 'Güncelle' : 'Ekle'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ShoppingListDetail; 