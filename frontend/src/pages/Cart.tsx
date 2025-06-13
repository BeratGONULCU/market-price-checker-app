import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Container, Typography } from '@mui/material';

const Cart: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate('/login', { state: { from: '/cart' } });
    }
  }, [user, navigate]);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Sepetim
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Sepet özelliği yakında eklenecek...
      </Typography>
    </Container>
  );
};

export default Cart; 