import React, { useState, useEffect } from 'react';
import {
    Box,
    Button,
    Card,
    CardContent,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Grid,
    IconButton,
    List,
    ListItem,
    ListItemText,
    TextField,
    Typography,
    MenuItem,
    InputAdornment,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon, Search as SearchIcon } from '@mui/icons-material';
import axios from 'axios';
import { Product, Category } from '../types';

const ProductManagement: React.FC = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [categories, setCategories] = useState<Category[]>([]);
    const [openDialog, setOpenDialog] = useState(false);
    const [editingProduct, setEditingProduct] = useState<Product | null>(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCategory, setSelectedCategory] = useState<number | ''>('');

    // Form state
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [brand, setBrand] = useState('');
    const [barcode, setBarcode] = useState('');
    const [imageUrl, setImageUrl] = useState('');
    const [categoryId, setCategoryId] = useState<number | ''>('');

    useEffect(() => {
        fetchProducts();
        fetchCategories();
    }, []);

    const fetchProducts = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/products');
            setProducts(response.data);
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    };

    const fetchCategories = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/categories');
            setCategories(response.data);
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const productData = {
                name,
                description,
                brand,
                barcode,
                image_url: imageUrl,
                category_id: categoryId
            };

            if (editingProduct) {
                await axios.put(`http://localhost:8000/api/v1/products/${editingProduct.id}`, productData);
            } else {
                await axios.post('http://localhost:8000/api/v1/products', productData);
            }

            fetchProducts();
            handleCloseDialog();
        } catch (error) {
            console.error('Error saving product:', error);
        }
    };

    const handleEdit = (product: Product) => {
        setEditingProduct(product);
        setName(product.name);
        setDescription(product.description || '');
        setBrand(product.brand || '');
        setBarcode(product.barcode || '');
        setImageUrl(product.image_url || '');
        setCategoryId(product.category?.id || '');
        setOpenDialog(true);
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Bu ürünü silmek istediğinizden emin misiniz?')) {
            try {
                await axios.delete(`http://localhost:8000/api/v1/products/${id}`);
                fetchProducts();
            } catch (error) {
                console.error('Error deleting product:', error);
            }
        }
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        setEditingProduct(null);
        setName('');
        setDescription('');
        setBrand('');
        setBarcode('');
        setImageUrl('');
        setCategoryId('');
    };

    const filteredProducts = products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (product.brand && product.brand.toLowerCase().includes(searchTerm.toLowerCase())) ||
            (product.barcode && product.barcode.toLowerCase().includes(searchTerm.toLowerCase()));
        const matchesCategory = selectedCategory === '' || product.category?.id === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    return (
        <Box sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h4">Ürün Yönetimi</Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setOpenDialog(true)}
                >
                    Yeni Ürün
                </Button>
            </Box>

            <Box sx={{ mb: 3 }}>
                <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                        <TextField
                            fullWidth
                            label="Ürün Ara"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <SearchIcon />
                                    </InputAdornment>
                                ),
                            }}
                        />
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <TextField
                            fullWidth
                            select
                            label="Kategori Filtrele"
                            value={selectedCategory}
                            onChange={(e) => setSelectedCategory(e.target.value as number | '')}
                        >
                            <MenuItem value="">Tümü</MenuItem>
                            {categories.map((category) => (
                                <MenuItem key={category.id} value={category.id}>
                                    {category.name}
                                </MenuItem>
                            ))}
                        </TextField>
                    </Grid>
                </Grid>
            </Box>

            <Grid container spacing={3}>
                {filteredProducts.map((product) => (
                    <Grid item xs={12} sm={6} md={4} key={product.id}>
                        <Card>
                            <CardContent>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                    <Typography variant="h6" component="div">
                                        {product.name}
                                    </Typography>
                                    <Box>
                                        <IconButton onClick={() => handleEdit(product)} size="small">
                                            <EditIcon />
                                        </IconButton>
                                        <IconButton onClick={() => handleDelete(product.id)} size="small">
                                            <DeleteIcon />
                                        </IconButton>
                                    </Box>
                                </Box>
                                {product.description && (
                                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                                        {product.description}
                                    </Typography>
                                )}
                                {product.brand && (
                                    <Typography variant="body2" color="text.secondary">
                                        Marka: {product.brand}
                                    </Typography>
                                )}
                                {product.barcode && (
                                    <Typography variant="body2" color="text.secondary">
                                        Barkod: {product.barcode}
                                    </Typography>
                                )}
                                {product.category && (
                                    <Typography variant="body2" color="text.secondary">
                                        Kategori: {product.category.name}
                                    </Typography>
                                )}
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
                <DialogTitle>
                    {editingProduct ? 'Ürün Düzenle' : 'Yeni Ürün Ekle'}
                </DialogTitle>
                <form onSubmit={handleSubmit}>
                    <DialogContent>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    label="Ürün Adı"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    required
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    label="Açıklama"
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                    multiline
                                    rows={3}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Marka"
                                    value={brand}
                                    onChange={(e) => setBrand(e.target.value)}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Barkod"
                                    value={barcode}
                                    onChange={(e) => setBarcode(e.target.value)}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    label="Resim URL"
                                    value={imageUrl}
                                    onChange={(e) => setImageUrl(e.target.value)}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    select
                                    label="Kategori"
                                    value={categoryId}
                                    onChange={(e) => setCategoryId(e.target.value as number | '')}
                                    required
                                >
                                    {categories.map((category) => (
                                        <MenuItem key={category.id} value={category.id}>
                                            {category.name}
                                        </MenuItem>
                                    ))}
                                </TextField>
                            </Grid>
                        </Grid>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleCloseDialog}>İptal</Button>
                        <Button type="submit" variant="contained">
                            {editingProduct ? 'Güncelle' : 'Ekle'}
                        </Button>
                    </DialogActions>
                </form>
            </Dialog>
        </Box>
    );
};

export default ProductManagement; 