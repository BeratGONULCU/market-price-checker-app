import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    Box,
    Typography,
    Button,
    List,
    ListItem,
    ListItemText,
    IconButton,
    TextField,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Paper,
    Grid,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { ShoppingListWithItems, Product, ShoppingListItemWithProduct } from '../types';
import axios from 'axios';

const ShoppingListDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [list, setList] = useState<ShoppingListWithItems | null>(null);
    const [products, setProducts] = useState<Product[]>([]);
    const [productNames, setProductNames] = useState<{[key: number]: string}>({});
    const [openDialog, setOpenDialog] = useState(false);
    const [selectedProduct, setSelectedProduct] = useState<number | ''>('');
    const [quantity, setQuantity] = useState<number>(1);
    const [notes, setNotes] = useState<string>('');

    useEffect(() => {
        if (id) {
            fetchListDetails();
            fetchProducts();
        }
    }, [id]);

    const fetchListDetails = async () => {
        try {
            const response = await fetch(`/api/shopping-lists/${id}`);
            const data = await response.json();
            setList(data);
            
            // Ürün adlarını çek
            if (data.items && data.items.length > 0) {
                await fetchProductNames(data.items.map((item: any) => item.product_id));
            }
        } catch (error) {
            console.error('Error fetching list details:', error);
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
            const response = await fetch('/api/products');
            const data = await response.json();
            setProducts(data);
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    };

    const handleAddItem = async () => {
        if (!selectedProduct) return;
        
        try {
            const response = await fetch(`/api/shopping-lists/${id}/items`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_id: selectedProduct,
                    quantity,
                    notes,
                }),
            });
            if (response.ok) {
                // Yeni ürünün adını çek
                await fetchProductNames([selectedProduct as number]);
                
                setOpenDialog(false);
                setSelectedProduct('');
                setQuantity(1);
                setNotes('');
                fetchListDetails();
            }
        } catch (error) {
            console.error('Error adding item:', error);
        }
    };

    const handleDeleteItem = async (itemId: number) => {
        if (window.confirm('Bu ürünü listeden silmek istediğinizden emin misiniz?')) {
            try {
                const response = await fetch(`/api/shopping-lists/${id}/items/${itemId}`, {
                    method: 'DELETE',
                });
                if (response.ok) {
                    fetchListDetails();
                }
            } catch (error) {
                console.error('Error deleting item:', error);
            }
        }
    };

    if (!list) {
        return <Typography>Yükleniyor...</Typography>;
    }

    return (
        <Box sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <IconButton onClick={() => navigate('/shopping-lists')} sx={{ mr: 2 }}>
                    <ArrowBackIcon />
                </IconButton>
                <Typography variant="h4">{list.name}</Typography>
            </Box>

            <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => setOpenDialog(true)}
                sx={{ mb: 3 }}
            >
                Ürün Ekle
            </Button>

            <List>
                {list.items?.map((item: ShoppingListItemWithProduct) => (
                    <Paper
                        key={item.id}
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
                                <IconButton
                                    edge="end"
                                    onClick={() => handleDeleteItem(item.id)}
                                >
                                    <DeleteIcon />
                                </IconButton>
                            }
                        >
                            <ListItemText
                                primary={getProductName(item.product_id)}
                                secondary={
                                    <>
                                        <Typography component="span" variant="body2">
                                            Miktar: {item.quantity}
                                        </Typography>
                                        {item.notes && (
                                            <Typography component="span" variant="body2" display="block">
                                                Not: {item.notes}
                                            </Typography>
                                        )}
                                    </>
                                }
                            />
                        </ListItem>
                    </Paper>
                ))}
            </List>

            <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
                <DialogTitle>Ürün Ekle</DialogTitle>
                <DialogContent>
                    <Grid container spacing={2} sx={{ mt: 1 }}>
                        <Grid item xs={12}>
                            <FormControl fullWidth>
                                <InputLabel>Ürün</InputLabel>
                                <Select
                                    value={selectedProduct}
                                    label="Ürün"
                                    onChange={(e) => setSelectedProduct(e.target.value as number)}
                                >
                                    {products.map((product) => (
                                        <MenuItem key={product.id} value={product.id}>
                                            {product.name}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                type="number"
                                label="Miktar"
                                value={quantity}
                                onChange={(e) => setQuantity(Number(e.target.value))}
                                inputProps={{ min: 1 }}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                label="Notlar"
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                                multiline
                                rows={2}
                            />
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenDialog(false)}>İptal</Button>
                    <Button onClick={handleAddItem} variant="contained">
                        Ekle
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default ShoppingListDetail; 