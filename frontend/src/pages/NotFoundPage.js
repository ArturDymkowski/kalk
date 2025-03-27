import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Container, Typography } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';

const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '70vh',
          textAlign: 'center',
        }}
      >
        <Typography variant="h1" color="primary" sx={{ fontSize: '8rem', fontWeight: 700 }}>
          404
        </Typography>
        <Typography variant="h4" gutterBottom>
          Strona nie została znaleziona
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Przepraszamy, nie możemy znaleźć strony, której szukasz. Być może adres URL został
          zmieniony lub strona została usunięta.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          size="large"
          startIcon={<HomeIcon />}
          onClick={() => navigate('/')}
          sx={{ mt: 2 }}
        >
          Wróć do strony głównej
        </Button>
      </Box>
    </Container>
  );
};

export default NotFoundPage;
