import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const Favorites: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Typography variant="h4">
        Favorilerim
      </Typography>
      <Box>
        {/* Favori ürünler listesi buraya gelecek */}
      </Box>
    </Container>
  );
};

export default Favorites; 