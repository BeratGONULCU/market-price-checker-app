import React, { useState } from 'react';
import {
  BottomNavigation,
  BottomNavigationAction,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Box,
  useTheme,
  useMediaQuery,
  AppBar,
  Toolbar,
  Typography,
} from '@mui/material';
import {
  Home,
  Favorite,
  CompareArrows,
  Store,
  Category,
  Person,
  Menu as MenuIcon,
  Search,
  Notifications,
  ShoppingCart,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const Navigation: React.FC = () => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const menuItems = [
    { text: 'Ana Sayfa', icon: <Home />, path: '/' },
    { text: 'Favoriler', icon: <Favorite />, path: '/favorites' },
    { text: 'Karşılaştır', icon: <CompareArrows />, path: '/compare' },
    { text: 'Marketler', icon: <Store />, path: '/markets' },
    { text: 'Kategoriler', icon: <Category />, path: '/categories' },
    { text: 'Alışveriş Listeleri', icon: <ShoppingCart />, path: '/shopping-lists' },
    { text: 'Profil', icon: <Person />, path: '/profile' },
  ];

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    setDrawerOpen(false);
  };

  const drawer = (
    <Box sx={{ width: 250 }} role="presentation">
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            onClick={() => handleNavigation(item.path)}
            selected={location.pathname === item.path}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      {/* AppBar with hamburger menu */}
      <AppBar position="fixed" sx={{ top: 0, bottom: 'auto' }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Market Fiyat Karşılaştırma
          </Typography>
          <IconButton color="inherit">
            <Search />
          </IconButton>
          <IconButton color="inherit">
            <Notifications />
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* Drawer (hamburger menu) */}
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={handleDrawerToggle}
        sx={{
          '& .MuiDrawer-paper': {
            width: 250,
            boxSizing: 'border-box',
          },
        }}
      >
        {drawer}
      </Drawer>

      {/* Bottom Navigation */}
      <BottomNavigation
        value={location.pathname}
        onChange={(event, newValue) => {
          handleNavigation(newValue);
        }}
        sx={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          right: 0,
          zIndex: 1000,
          display: { xs: 'flex', sm: 'none' }, // Sadece mobilde göster
        }}
      >
        <BottomNavigationAction
          label="Ana Sayfa"
          value="/"
          icon={<Home />}
        />
        <BottomNavigationAction
          label="Favoriler"
          value="/favorites"
          icon={<Favorite />}
        />
        <BottomNavigationAction
          label="Listeler"
          value="/shopping-lists"
          icon={<ShoppingCart />}
        />
        <BottomNavigationAction
          label="Profil"
          value="/profile"
          icon={<Person />}
        />
      </BottomNavigation>

      {/* Content padding for fixed AppBar and BottomNavigation */}
      <Box
        sx={{
          mt: { xs: '56px', sm: '64px' }, // AppBar height
          mb: { xs: '56px', sm: 0 }, // BottomNavigation height
        }}
      />
    </>
  );
};

export default Navigation; 