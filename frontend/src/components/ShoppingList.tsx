import React, { useState, useEffect } from 'react';
import { 
    Box, 
    Typography, 
    Button, 
    List, 
    ListItem, 
    ListItemText, 
    IconButton,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Paper
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import { ShoppingList as ShoppingListType, ShoppingListWithItems } from '../types';
import { useNavigate } from 'react-router-dom';

const ShoppingList: React.FC = () => {
    const [lists, setLists] = useState<ShoppingListWithItems[]>([]);
    const [openDialog, setOpenDialog] = useState(false);
    const [newListName, setNewListName] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchLists();
    }, []);

    const fetchLists = async () => {
        try {
            const response = await fetch('/api/shopping-lists');
            const data = await response.json();
            setLists(data);
        } catch (error) {
            console.error('Error fetching shopping lists:', error);
        }
    };

    const handleCreateList = async () => {
        try {
            const response = await fetch('/api/shopping-lists', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: newListName }),
            });
            if (response.ok) {
                setOpenDialog(false);
                setNewListName('');
                fetchLists();
            }
        } catch (error) {
            console.error('Error creating shopping list:', error);
        }
    };

    const handleDeleteList = async (listId: number) => {
        if (window.confirm('Bu listeyi silmek istediğinizden emin misiniz?')) {
            try {
                const response = await fetch(`/api/shopping-lists/${listId}`, {
                    method: 'DELETE',
                });
                if (response.ok) {
                    fetchLists();
                }
            } catch (error) {
                console.error('Error deleting shopping list:', error);
            }
        }
    };

    return (
        <Box sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h4">Alışveriş Listeleri</Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setOpenDialog(true)}
                >
                    Yeni Liste
                </Button>
            </Box>

            <List>
                {lists.map((list) => (
                    <Paper
                        key={list.id}
                        sx={{
                            mb: 2,
                            p: 2,
                            '&:hover': {
                                boxShadow: 3,
                            },
                        }}
                    >
                        <ListItem
                            secondaryAction={
                                <Box>
                                    <IconButton
                                        edge="end"
                                        onClick={() => navigate(`/shopping-lists/${list.id}`)}
                                    >
                                        <EditIcon />
                                    </IconButton>
                                    <IconButton
                                        edge="end"
                                        onClick={() => handleDeleteList(list.id)}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </Box>
                            }
                        >
                            <ListItemText
                                primary={list.name}
                                secondary={`${list.items?.length || 0} ürün`}
                            />
                        </ListItem>
                    </Paper>
                ))}
            </List>

            <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
                <DialogTitle>Yeni Alışveriş Listesi</DialogTitle>
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
                    <Button onClick={() => setOpenDialog(false)}>İptal</Button>
                    <Button onClick={handleCreateList} variant="contained">
                        Oluştur
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default ShoppingList; 