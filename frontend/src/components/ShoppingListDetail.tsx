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
    Card,
    CardContent,
    Chip,
    Alert,
    CircularProgress
} from '@mui/material';
import { 
    Add as AddIcon, 
    Delete as DeleteIcon, 
    ArrowBack as ArrowBackIcon,
    ShoppingCart as ShoppingCartIcon,
    LocationOn as LocationOnIcon
} from '@mui/icons-material';
import { ShoppingListWithItems, Product, ShoppingListItemWithProduct } from '../types';
import axios from 'axios';

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
    const [marketComparisons, setMarketComparisons] = useState<MarketComparison[]>([]);
    const [showMarketComparison, setShowMarketComparison] = useState(false);
    const [selectedMarket, setSelectedMarket] = useState<MarketComparison | null>(null);
    const [loadingMarkets, setLoadingMarkets] = useState(false);

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

    const fetchMarketComparisons = async () => {
        if (!id) return;
        
        try {
            setLoadingMarkets(true);
            const response = await axios.get(`http://localhost:8000/api/v1/shopping-lists/${id}/market-comparison`);
            setMarketComparisons(response.data);
            setShowMarketComparison(true);
        } catch (error) {
            console.error('Error fetching market comparisons:', error);
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
        if (!list || list.items?.length === 0) {
            alert('Alışveriş listenizde ürün bulunmamaktadır');
            return;
        }
        fetchMarketComparisons();
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
                    disabled={!list || list.items?.length === 0}
                >
                    Bu Listeyi Satın Al
                </Button>
            </Box>

            {list.items?.length === 0 ? (
                <Alert severity="info">
                    Bu listede henüz ürün bulunmamaktadır. Alışverişe başlamak için ürün ekleyin.
                </Alert>
            ) : (
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
            )}

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
                                                {market.items.length} ürün bulundu
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
        </Box>
    );
};

export default ShoppingListDetail; 