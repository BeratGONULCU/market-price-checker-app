import React from 'react';
import { Container, Typography } from '@mui/material';

const Cart: React.FC = () => {
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