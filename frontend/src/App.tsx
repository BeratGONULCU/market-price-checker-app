import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
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
import PrivateRoute from './components/PrivateRoute';
import Cart from './pages/Cart';

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/favorites" element={<Favorites />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/markets" element={<Markets />} />
          <Route path="/categories" element={<Categories />} />
          <Route path="/markets/:id" element={<MarketDetail />} />
          <Route path="/favorites" element={<PrivateRoute><Favorites /></PrivateRoute>} />
          <Route path="/cart" element={<PrivateRoute><Cart /></PrivateRoute>} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App; 