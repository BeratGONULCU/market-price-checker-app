import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const Categories: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Typography variant="h4">
        Kategoriler
      </Typography>
      <Box>
        {/* Kategori listesi buraya gelecek */}
      </Box>
    </Container>
  );
};

export default Categories; 