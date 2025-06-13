import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import Favorites from './pages/Favorites';
import Compare from './pages/Compare';
import Markets from './pages/Markets';
import Categories from './pages/Categories';
import MarketDetail from './pages/MarketDetail';
import ProductDetail from './pages/ProductDetail';
import ShoppingList from './pages/ShoppingList';
import Cart from './pages/Cart';
import { useAuth } from './contexts/AuthContext';
import ShoppingLists from './pages/ShoppingLists';
import ShoppingListDetail from './pages/ShoppingListDetail';

// Auth Layout - Login ve Register sayfaları için
const AuthLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div style={{ 
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#f5f5f5'
    }}>
      {children}
    </div>
  );
};

// Main Layout - Diğer tüm sayfalar için
const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <>
      <Navigation />
      {children}
    </>
  );
};

// Auth Route - Login ve Register sayfaları için
const AuthRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  return user ? <Navigate to="/" /> : <AuthLayout>{children}</AuthLayout>;
};

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          {/* Auth Routes */}
          <Route path="/login" element={<AuthRoute><Login /></AuthRoute>} />
          <Route path="/register" element={<AuthRoute><Register /></AuthRoute>} />

          {/* Main Routes */}
          <Route path="/" element={
            <MainLayout>
              <Home />
            </MainLayout>
          } />
          <Route path="/profile" element={
            <MainLayout>
              <Profile />
            </MainLayout>
          } />
          <Route path="/favorites" element={
            <MainLayout>
              <Favorites />
            </MainLayout>
          } />
          <Route path="/compare" element={
            <MainLayout>
              <Compare />
            </MainLayout>
          } />
          <Route path="/markets" element={
            <MainLayout>
              <Markets />
            </MainLayout>
          } />
          <Route path="/categories" element={
            <MainLayout>
              <Categories />
            </MainLayout>
          } />
          <Route path="/markets/:id" element={
            <MainLayout>
              <MarketDetail />
            </MainLayout>
          } />
          <Route path="/products/:id" element={
            <MainLayout>
              <ProductDetail />
            </MainLayout>
          } />
          <Route path="/shopping-list" element={
            <MainLayout>
              <ShoppingList />
            </MainLayout>
          } />
          <Route path="/cart" element={
            <MainLayout>
              <Cart />
            </MainLayout>
          } />
          <Route path="/shopping-lists" element={
            <MainLayout>
              <ShoppingLists />
            </MainLayout>
          } />
          <Route path="/shopping-lists/:id" element={
            <MainLayout>
              <ShoppingListDetail />
            </MainLayout>
          } />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;