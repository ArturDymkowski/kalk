import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Divider,
  Grid,
  Typography,
  useTheme,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ListAltIcon from '@mui/icons-material/ListAlt';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import { useAppContext } from '../contexts/AppContext';

const HomePage = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const { hasCharts } = useAppContext();

  const features = [
    {
      title: 'Kosmogramy i Vargi',
      description: 'Obliczanie dokładnych kosmogramów D1-D12 według zasad klasycznej astrologii wedyjskiej.',
      icon: '🔮'
    },
    {
      title: 'Analiza obszarów życia',
      description: 'Szczegółowa analiza różnych obszarów życia: zdrowia, finansów, związków, kariery i talentów.',
      icon: '📊'
    },
    {
      title: 'Sztuczna inteligencja',
      description: 'Wykorzystanie AI do profesjonalnej interpretacji Twojego kosmogramu wedyjskiego.',
      icon: '🤖'
    }
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4, textAlign: 'center' }}>
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{
            fontWeight: 700,
            color: theme.palette.primary.main,
          }}
        >
          Kalkulator Astrologii Wedyjskiej
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Odkryj swój los zapisany w gwiazdach dzięki precyzyjnym obliczeniom astrologicznym
        </Typography>
        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center', gap: 2 }}>
          <Button
            variant="contained"
            size="large"
            startIcon={<AddIcon />}
            onClick={() => navigate('/charts/new')}
          >
            Nowy kosmogram
          </Button>
          <Button
            variant="outlined"
            size="large"
            startIcon={<ListAltIcon />}
            onClick={() => navigate('/charts')}
          >
            Lista kosmogramów
          </Button>
        </Box>
      </Box>

      <Box sx={{ my: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom align="center">
          Główne funkcje
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h2" align="center" gutterBottom>
                    {feature.icon}
                  </Typography>
                  <Typography variant="h6" component="h3" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Divider sx={{ my: 6 }} />

      <Box sx={{ my: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom align="center">
          Jak to działa?
        </Typography>
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center', p: 2 }}>
              <Typography variant="h6" gutterBottom>
                1. Wprowadź dane urodzenia
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Podaj swoją datę, godzinę i miejsce urodzenia, aby otrzymać precyzyjny kosmogram.
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center', p: 2 }}>
              <Typography variant="h6" gutterBottom>
                2. Sprawdź swój kosmogram
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Przeglądaj 12 różnych varg (D1-D12) przedstawiających różne aspekty Twojego życia.
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center', p: 2 }}>
              <Typography variant="h6" gutterBottom>
                3. Wykonaj analizę
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Wybierz interesujący Cię obszar życia i otrzymaj szczegółową analizę opartą na Twoim kosmogramie.
              </Typography>
            </Box>
          </Grid>
        </Grid>
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Button
            variant="contained"
            size="large"
            color="primary"
            startIcon={<AddIcon />}
            onClick={() => navigate('/charts/new')}
          >
            Rozpocznij teraz
          </Button>
        </Box>
      </Box>

      {hasCharts && (
        <Box sx={{ my: 6 }}>
          <Typography variant="h5" component="h2" gutterBottom align="center">
            Masz już utworzone kosmogramy
          </Typography>
          <Box sx={{ mt: 3, textAlign: 'center' }}>
            <Button
              variant="outlined"
              size="large"
              startIcon={<AnalyticsIcon />}
              onClick={() => navigate('/charts')}
            >
              Przejdź do swoich kosmogramów
            </Button>
          </Box>
        </Box>
      )}
    </Container>
  );
};

export default HomePage;
