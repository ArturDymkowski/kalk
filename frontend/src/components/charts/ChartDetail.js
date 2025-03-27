import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Paper,
  Tab,
  Tabs,
  Typography,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
} from '@mui/material';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import PlanetIcon from '@mui/icons-material/Public';
import { chartsApi } from '../../api/apiClient';
import ChartVisualization from './ChartVisualization';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';
import { format } from 'date-fns';
import { pl } from 'date-fns/locale';

// TabPanel component for tabs
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`chart-tabpanel-${index}`}
      aria-labelledby={`chart-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const ChartDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [chart, setChart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);

  // Varga tabs mapping
  const vargaTabs = [
    { id: 'D1', label: 'D1 - Rashi', description: 'Główna mapa życia' },
    { id: 'D2', label: 'D2 - Hora', description: 'Bogactwo i finanse' },
    { id: 'D3', label: 'D3 - Drekkana', description: 'Rodzeństwo i motywacja' },
    { id: 'D4', label: 'D4 - Chaturtamsa', description: 'Nieruchomości i luksus' },
    { id: 'D5', label: 'D5 - Panchamsa', description: 'Kreatywność i zasługi' },
    { id: 'D6', label: 'D6 - Shashtamsa', description: 'Zdrowie i choroby' },
    { id: 'D7', label: 'D7 - Saptamsa', description: 'Dzieci i płodność' },
    { id: 'D8', label: 'D8 - Ashtamsa', description: 'Nagłe zmiany, transformacje' },
    { id: 'D9', label: 'D9 - Navamsa', description: 'Związki i dharma' },
    { id: 'D10', label: 'D10 - Dasamsa', description: 'Kariera i sukces zawodowy' },
    { id: 'D11', label: 'D11 - Ekadasamsa', description: 'Przyjaciele i zyski' },
    { id: 'D12', label: 'D12 - Dvadasamsa', description: 'Rodzice i karma rodowa' },
  ];

  useEffect(() => {
    const fetchChart = async () => {
      try {
        setLoading(true);
        const chartData = await chartsApi.getChart(id);
        setChart(chartData);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch chart details:', err);
        setError(
          err.response?.data?.error || 'Nie udało się pobrać szczegółów kosmogramu.'
        );
      } finally {
        setLoading(false);
      }
    };

    fetchChart();
  }, [id]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  // Format birth date
  const formatBirthDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return format(date, "d MMMM yyyy 'o' HH:mm", { locale: pl });
    } catch (e) {
      return dateString;
    }
  };

  if (loading) {
    return <Loading message="Pobieranie szczegółów kosmogramu..." />;
  }

  if (error) {
    return (
      <Box>
        <Button
          variant="outlined"
          startIcon={<ChevronLeftIcon />}
          onClick={() => navigate('/charts')}
          sx={{ mb: 2 }}
        >
          Powrót do listy
        </Button>
        <ErrorMessage message={error} />
      </Box>
    );
  }

  if (!chart) {
    return (
      <Box>
        <Button
          variant="outlined"
          startIcon={<ChevronLeftIcon />}
          onClick={() => navigate('/charts')}
          sx={{ mb: 2 }}
        >
          Powrót do listy
        </Button>
        <Typography variant="h6">Kosmogram nie został znaleziony</Typography>
      </Box>
    );
  }

  const currentVarga = vargaTabs[tabValue].id;
  const vargaData = chart.vargas && chart.vargas[currentVarga];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Button
            variant="outlined"
            startIcon={<ChevronLeftIcon />}
            onClick={() => navigate('/charts')}
            sx={{ mb: 1 }}
          >
            Powrót do listy
          </Button>
          <Typography variant="h4" component="h1">
            {chart.name}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {formatBirthDate(chart.birth_date)}
          </Typography>
        </Box>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AnalyticsIcon />}
          onClick={() => navigate(`/analysis/${chart.id}`)}
        >
          Analizuj kosmogram
        </Button>
      </Box>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Data i godzina urodzenia
              </Typography>
              <Typography variant="body1">
                {formatBirthDate(chart.birth_date)}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Współrzędne geograficzne
              </Typography>
              <Typography variant="body1">
                Szerokość: {chart.latitude.toFixed(4)}, Długość: {chart.longitude.toFixed(4)}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Paper sx={{ width: '100%', mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          aria-label="chart vargas tabs"
        >
          {vargaTabs.map((tab, index) => (
            <Tab
              key={tab.id}
              label={tab.label}
              id={`chart-tab-${index}`}
              aria-controls={`chart-tabpanel-${index}`}
            />
          ))}
        </Tabs>

        {vargaTabs.map((tab, index) => (
          <TabPanel key={tab.id} value={tabValue} index={index}>
            <Box sx={{ mb: 2 }}>
              <Typography variant="h6">{tab.label}</Typography>
              <Typography variant="body2" color="text.secondary">
                {tab.description}
              </Typography>
            </Box>

            <Divider sx={{ mb: 3 }} />

            {chart.vargas && chart.vargas[tab.id] ? (
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <ChartVisualization
                    chartData={chart.vargas[tab.id]}
                    vargaType={tab.id}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Pozycje planet
                  </Typography>
                  <List>
                    {Object.entries(chart.vargas[tab.id].planets).map(([planet, data]) => (
                      <ListItem key={planet} divider>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <PlanetIcon sx={{ mr: 1 }} />
                              {planet}
                            </Box>
                          }
                          secondary={`${data.sign_name} ${data.degrees_in_sign.toFixed(2)}°`}
                        />
                        <Chip
                          label={data.sign_name}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                      </ListItem>
                    ))}
                  </List>
                </Grid>
              </Grid>
            ) : (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <CircularProgress size={40} />
                <Typography variant="body2" sx={{ mt: 2 }}>
                  Ładowanie danych vargi...
                </Typography>
              </Box>
            )}
          </TabPanel>
        ))}
      </Paper>
    </Box>
  );
};

export default ChartDetail;
