import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  CircularProgress,
  Avatar,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { useSnackbar } from 'notistack';
import axios from 'axios';
import { User } from '../types/index';

const Profile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
    try {
      setLoading(true);
      const response = await axios.get<User>('http://localhost:8000/api/v1/users/me');
      setUser(response.data);
      setName(response.data.name);
      setEmail(response.data.email);
      setImageUrl(response.data.image_url || '');
    } catch (error) {
      console.error('Error fetching user:', error);
      enqueueSnackbar('Kullanıcı bilgileri yüklenirken hata oluştu', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async () => {
    try {
      const response = await axios.put<User>('http://localhost:8000/api/v1/users/me', {
        name,
        email,
        image_url: imageUrl
      });
      setUser(response.data);
      setOpenDialog(false);
      enqueueSnackbar('Profil güncellendi', { variant: 'success' });
    } catch (error) {
      console.error('Error updating profile:', error);
      enqueueSnackbar('Profil güncellenirken hata oluştu', { variant: 'error' });
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!user) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Yükleniyor...</Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Profil Bilgilerim
      </Typography>
      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={3}>
            <Avatar
              sx={{ width: 100, height: 100, mr: 3 }}
              src={user.image_url}
            />
            <Box>
              <Typography variant="h5">{user.name}</Typography>
              <Typography variant="body1" color="text.secondary">
                {user.email}
              </Typography>
            </Box>
          </Box>
          <Divider sx={{ my: 3 }} />
          <Button
            variant="contained"
            onClick={() => setOpenDialog(true)}
          >
            Profili Düzenle
          </Button>
        </CardContent>
      </Card>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Profili Düzenle</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Ad Soyad"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="E-posta"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Profil Resmi URL"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>İptal</Button>
          <Button onClick={handleUpdateProfile} variant="contained">
            Kaydet
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Profile; 