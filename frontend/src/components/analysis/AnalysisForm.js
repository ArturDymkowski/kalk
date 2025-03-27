import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Divider,
  FormControl,
  FormHelperText,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  Alert,
} from '@mui/material';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import { chartsApi, lifeAreasApi, analysisApi } from '../../api/apiClient';
import { useAppContext } from '../../contexts/AppContext';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const AnalysisForm = () => {
  const { chartId } = useParams();
  const navigate = useNavigate();
  const { lifeAreas } = useAppContext();
  
  const [selectedLifeArea, setSelectedLifeArea] = useState('');
  const [chart, setChart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [resultError, setResultError] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    const fetchChart = async () => {
      try {
        setLoading(true);
        const chartData = await chartsApi.getChart(chartId);
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
  }, [chartId]);

  const handleLifeAreaChange = (event) => {
    setSelectedLifeArea(event.target.value);
  };

  const handleAnalyze = async () => {
    if (!selectedLifeArea) {
      return;
    }

    try {
      setAnalyzing(true);
      setResultError(null);
      
      const result = await analysisApi.analyzeChart(parseInt(chartId), parseInt(selectedLifeArea));
      
      if (result && result.analysis_result) {
        setAnalysis(result);
      } else {
        setResultError('Nie otrzymano wyników analizy.');
      }
    } catch (err) {
      console.error('Analysis failed:', err);
      setResultError(
        err.response?.data?.error || 'Analiza nie powiodła się. Spróbuj ponownie.'
      );
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return <Loading message="Ładowanie danych kosmogramu..." />;
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

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Button
          variant="outlined"
          startIcon={<ChevronLeftIcon />}
          onClick={() => navigate(`/charts/${chartId}`)}
          sx={{ mr: 2 }}
        >
          Powrót do kosmogramu
        </Button>
        <Typography variant="h4" component="h1">
          Analiza kosmogramu
        </Typography>
      </Box>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            {chart.name}
          </Typography>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Wybierz obszar życia do analizy
          </Typography>

          <Divider sx={{ my: 2 }} />

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth error={!selectedLifeArea}>
                <InputLabel id="life-area-select-label">Obszar życia</InputLabel>
                <Select
                  labelId="life-area-select-label"
                  value={selectedLifeArea}
                  label="Obszar życia"
                  onChange={handleLifeAreaChange}
                  disabled={analyzing}
                >
                  {lifeAreas.map((area) => (
                    <MenuItem key={area.id} value={area.id}>
                      {area.name} ({area.varga_combination})
                    </MenuItem>
                  ))}
                </Select>
                {!selectedLifeArea && (
                  <FormHelperText>Wybierz obszar życia do analizy</FormHelperText>
                )}
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                size="large"
                startIcon={analyzing ? <CircularProgress size={20} color="inherit" /> : <AnalyticsIcon />}
                onClick={handleAnalyze}
                disabled={!selectedLifeArea || analyzing}
                sx={{ height: '56px' }} // Match the height of Select
              >
                {analyzing ? 'Analizowanie...' : 'Analizuj kosmogram'}
              </Button>
            </Grid>
          </Grid>

          {selectedLifeArea && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary">
                {lifeAreas.find((area) => area.id === parseInt(selectedLifeArea))?.description || ''}
              </Typography>
            </Box>
          )}

          {resultError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {resultError}
            </Alert>
          )}
        </CardContent>
      </Card>

      {analysis && (
        <Card>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Wynik analizy: {lifeAreas.find((area) => area.id === analysis.life_area_id)?.name}
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Typography
              variant="body1"
              component="div"
              sx={{
                whiteSpace: 'pre-line',
                '& p': { marginBottom: '1em' },
              }}
            >
              {analysis.analysis_result}
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default AnalysisForm;
