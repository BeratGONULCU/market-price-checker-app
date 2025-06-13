import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
  Paper
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon, ShoppingCart as ShoppingCartIcon } from '@mui/icons-material';
import { useSnackbar } from 'notistack';
import { useAuth } from '../contexts/AuthContext';
import shoppingListService from '../services/shoppingList';
import { ShoppingList } from '../types/shoppingList';

const ShoppingLists: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { enqueueSnackbar } = useSnackbar();
  const [lists, setLists] = useState<ShoppingList[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [listName, setListName] = useState('');
  const [editingList, setEditingList] = useState<ShoppingList | null>(null);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    loadLists();
  }, [user, navigate]);

  const loadLists = async () => {
    try {
      const data = await shoppingListService.getShoppingLists();
      setLists(data);
    } catch (error) {
      enqueueSnackbar('Alışveriş listeleri yüklenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleCreateList = async () => {
    try {
      await shoppingListService.createShoppingList(listName);
      enqueueSnackbar('Alışveriş listesi oluşturuldu', { variant: 'success' });
      setOpenDialog(false);
      setListName('');
      loadLists();
    } catch (error) {
      enqueueSnackbar('Alışveriş listesi oluşturulurken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleUpdateList = async () => {
    if (!editingList) return;
    try {
      await shoppingListService.updateShoppingList(editingList.id, listName);
      enqueueSnackbar('Alışveriş listesi güncellendi', { variant: 'success' });
      setOpenDialog(false);
      setListName('');
      setEditingList(null);
      loadLists();
    } catch (error) {
      enqueueSnackbar('Alışveriş listesi güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleDeleteList = async (id: number) => {
    if (!window.confirm('Bu alışveriş listesini silmek istediğinizden emin misiniz?')) return;
    try {
      await shoppingListService.deleteShoppingList(id);
      enqueueSnackbar('Alışveriş listesi silindi', { variant: 'success' });
      loadLists();
    } catch (error) {
      enqueueSnackbar('Alışveriş listesi silinirken bir hata oluştu', { variant: 'error' });
    }
  };

  const handleOpenDialog = (list?: ShoppingList) => {
    if (list) {
      setEditingList(list);
      setListName(list.name);
    } else {
      setEditingList(null);
      setListName('');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setListName('');
    setEditingList(null);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Alışveriş Listelerim
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Yeni Liste
        </Button>
      </Box>

      <Paper elevation={2}>
        <List>
          {lists.map((list) => (
            <ListItem
              key={list.id}
              button
              onClick={() => navigate(`/shopping-lists/${list.id}`)}
            >
              <ListItemText
                primary={list.name}
                secondary={`${list.items.length} ürün`}
              />
              <ListItemSecondaryAction>
                <IconButton
                  edge="end"
                  aria-label="edit"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleOpenDialog(list);
                  }}
                >
                  <EditIcon />
                </IconButton>
                <IconButton
                  edge="end"
                  aria-label="delete"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteList(list.id);
                  }}
                >
                  <DeleteIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      </Paper>

      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>
          {editingList ? 'Listeyi Düzenle' : 'Yeni Liste Oluştur'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Liste Adı"
            type="text"
            fullWidth
            value={listName}
            onChange={(e) => setListName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>İptal</Button>
          <Button
            onClick={editingList ? handleUpdateList : handleCreateList}
            color="primary"
            disabled={!listName.trim()}
          >
            {editingList ? 'Güncelle' : 'Oluştur'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ShoppingLists; 