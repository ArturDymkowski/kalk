import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import BirthChartForm from '../components/charts/BirthChartForm';

const ChartFormPage = () => {
  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Nowy kosmogram
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Wprowadź dokładne dane urodzenia, aby utworzyć kosmogram wedyjski. 
          Pamiętaj, że precyzja danych jest kluczowa dla poprawności obliczeń astrologicznych.
        </Typography>
        <BirthChartForm />
      </Box>
    </Container>
  );
};

export default ChartFormPage;
