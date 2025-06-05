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
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App; 