import React from 'react';
import { Link } from 'react-router-dom';
import {
  AppBar,
  Box,
  Button,
  Container,
  IconButton,
  Toolbar,
  Typography
} from '@mui/material';
import {
  Home as HomeIcon,
  Favorite as FavoriteIcon,
  ShoppingCart as ShoppingCartIcon,
  Person as PersonIcon,
  Logout as LogoutIcon,
  Login as LoginIcon,
  List as ListIcon
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <AppBar position="static">
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component={Link}
            to="/"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontWeight: 700,
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            Market Fiyat Takip
          </Typography>

          <Box sx={{ flexGrow: 1, display: 'flex', gap: 2 }}>
            <Button
              component={Link}
              to="/"
              color="inherit"
              startIcon={<HomeIcon />}
            >
              Ana Sayfa
            </Button>
            {user && (
              <>
                <Button
                  component={Link}
                  to="/favorites"
                  color="inherit"
                  startIcon={<FavoriteIcon />}
                >
                  Favoriler
                </Button>
                <Button
                  component={Link}
                  to="/shopping-lists"
                  color="inherit"
                  startIcon={<ListIcon />}
                >
                  Alışveriş Listeleri
                </Button>
                <Button
                  component={Link}
                  to="/cart"
                  color="inherit"
                  startIcon={<ShoppingCartIcon />}
                >
                  Sepet
                </Button>
              </>
            )}
          </Box>

          <Box sx={{ flexGrow: 0 }}>
            {user ? (
              <IconButton
                onClick={handleLogout}
                color="inherit"
                title="Çıkış Yap"
              >
                <LogoutIcon />
              </IconButton>
            ) : (
              <Button
                component={Link}
                to="/login"
                color="inherit"
                startIcon={<LoginIcon />}
              >
                Giriş Yap
              </Button>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar; 