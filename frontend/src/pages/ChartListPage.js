import React from 'react';
import { Container } from '@mui/material';
import ChartList from '../components/charts/ChartList';

const ChartListPage = () => {
  return (
    <Container maxWidth="lg">
      <ChartList />
    </Container>
  );
};

export default ChartListPage;
