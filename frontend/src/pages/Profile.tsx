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
  Divider
} from '@mui/material';
import { useSnackbar } from 'notistack';
import { User } from '../types';
import authService from '../services/auth';

const Profile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      const userData = await authService.getCurrentUser();
      setUser(userData);
      setFormData(prev => ({
        ...prev,
        name: userData.name,
        email: userData.email
      }));
    } catch (error) {
      console.error('Error fetching user profile:', error);
      enqueueSnackbar('Profil bilgileri yüklenirken bir hata oluştu', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (formData.password) {
        if (formData.password !== formData.confirmPassword) {
          enqueueSnackbar('Yeni şifreler eşleşmiyor', { variant: 'error' });
          return;
        }
      }

      await authService.updateProfile({
        name: formData.name,
        password: formData.password,
        email: formData.email
      });

      setEditing(false);
      enqueueSnackbar('Profil başarıyla güncellendi', { variant: 'success' });
      fetchUserProfile();
    } catch (error) {
      console.error('Error updating profile:', error);
      enqueueSnackbar('Profil güncellenirken bir hata oluştu', { variant: 'error' });
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
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
              src={user?.image_url}
            />
            <Box>
              <Typography variant="h5">{user?.name}</Typography>
              <Typography variant="body1" color="text.secondary">
                {user?.email}
              </Typography>
            </Box>
          </Box>
          <Divider sx={{ my: 3 }} />
          <form onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Ad Soyad"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  disabled={!editing}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="E-posta"
                  name="email"
                  value={formData.email}
                  disabled
                />
              </Grid>
              {editing && (
                <>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      type="password"
                      label="Yeni Şifre"
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      type="password"
                      label="Yeni Şifre (Tekrar)"
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleInputChange}
                    />
                  </Grid>
                </>
              )}
              <Grid item xs={12}>
                <Box display="flex" gap={2}>
                  {editing ? (
                    <>
                      <Button
                        variant="contained"
                        color="primary"
                        type="submit"
                      >
                        Kaydet
                      </Button>
                      <Button
                        variant="outlined"
                        onClick={() => {
                          setEditing(false);
                          setFormData(prev => ({
                            ...prev,
                            password: '',
                            confirmPassword: ''
                          }));
                        }}
                      >
                        İptal
                      </Button>
                    </>
                  ) : (
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => setEditing(true)}
                    >
                      Düzenle
                    </Button>
                  )}
                </Box>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Profile; 