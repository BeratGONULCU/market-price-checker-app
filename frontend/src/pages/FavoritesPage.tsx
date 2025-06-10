import React from 'react';
import { Container, Typography } from '@mui/material';

const FavoritesPage: React.FC = () => {
  console.log('FavoritesPage rendered');

  return (
    <Container>
      <Typography variant="h4" sx={{ mt: 4, mb: 4 }}>
        Favorilerim
      </Typography>
      <Typography variant="h6">
        Bu bir test mesajıdır.
      </Typography>
    </Container>
  );
};

export default FavoritesPage; 