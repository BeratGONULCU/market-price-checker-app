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
    Paper,
    Grid,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { Category } from '../types';

const CategoryManagement: React.FC = () => {
    const [categories, setCategories] = useState<Category[]>([]);
    const [openDialog, setOpenDialog] = useState(false);
    const [editingCategory, setEditingCategory] = useState<Category | null>(null);
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [parentId, setParentId] = useState<number | ''>('');

    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        try {
            const response = await fetch('/api/categories');
            const data = await response.json();
            setCategories(data);
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    };

    const handleSubmit = async () => {
        try {
            const categoryData = {
                name,
                description,
                parent_id: parentId || null,
            };

            const url = editingCategory
                ? `/api/categories/${editingCategory.id}`
                : '/api/categories';
            const method = editingCategory ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(categoryData),
            });

            if (response.ok) {
                setOpenDialog(false);
                resetForm();
                fetchCategories();
            }
        } catch (error) {
            console.error('Error saving category:', error);
        }
    };

    const handleEdit = (category: Category) => {
        setEditingCategory(category);
        setName(category.name);
        setDescription(category.description || '');
        setParentId(category.parent_id || '');
        setOpenDialog(true);
    };

    const handleDelete = async (categoryId: number) => {
        if (window.confirm('Bu kategoriyi silmek istediğinizden emin misiniz?')) {
            try {
                const response = await fetch(`/api/categories/${categoryId}`, {
                    method: 'DELETE',
                });
                if (response.ok) {
                    fetchCategories();
                }
            } catch (error) {
                console.error('Error deleting category:', error);
            }
        }
    };

    const resetForm = () => {
        setEditingCategory(null);
        setName('');
        setDescription('');
        setParentId('');
    };

    const handleClose = () => {
        setOpenDialog(false);
        resetForm();
    };

    return (
        <Box sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h4">Kategoriler</Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setOpenDialog(true)}
                >
                    Yeni Kategori
                </Button>
            </Box>

            <List>
                {categories.map((category) => (
                    <Paper
                        key={category.id}
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
                                        onClick={() => handleEdit(category)}
                                    >
                                        <EditIcon />
                                    </IconButton>
                                    <IconButton
                                        edge="end"
                                        onClick={() => handleDelete(category.id)}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </Box>
                            }
                        >
                            <ListItemText
                                primary={category.name}
                                secondary={
                                    <>
                                        {category.description && (
                                            <Typography component="span" variant="body2">
                                                {category.description}
                                            </Typography>
                                        )}
                                        {category.parent_id && (
                                            <Typography component="span" variant="body2" display="block">
                                                Üst Kategori: {
                                                    categories.find(c => c.id === category.parent_id)?.name
                                                }
                                            </Typography>
                                        )}
                                    </>
                                }
                            />
                        </ListItem>
                    </Paper>
                ))}
            </List>

            <Dialog open={openDialog} onClose={handleClose}>
                <DialogTitle>
                    {editingCategory ? 'Kategori Düzenle' : 'Yeni Kategori'}
                </DialogTitle>
                <DialogContent>
                    <Grid container spacing={2} sx={{ mt: 1 }}>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                label="Kategori Adı"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                label="Açıklama"
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                multiline
                                rows={2}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControl fullWidth>
                                <InputLabel>Üst Kategori</InputLabel>
                                <Select
                                    value={parentId}
                                    label="Üst Kategori"
                                    onChange={(e) => setParentId(e.target.value as number)}
                                >
                                    <MenuItem value="">Yok</MenuItem>
                                    {categories
                                        .filter(c => c.id !== editingCategory?.id)
                                        .map((category) => (
                                            <MenuItem key={category.id} value={category.id}>
                                                {category.name}
                                            </MenuItem>
                                        ))}
                                </Select>
                            </FormControl>
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>İptal</Button>
                    <Button onClick={handleSubmit} variant="contained">
                        {editingCategory ? 'Güncelle' : 'Oluştur'}
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default CategoryManagement; 