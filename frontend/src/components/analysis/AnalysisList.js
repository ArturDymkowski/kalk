import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
  Chip,
} from '@mui/material';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import { analysisApi } from '../../api/apiClient';
import { useAppContext } from '../../contexts/AppContext';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';
import { format } from 'date-fns';
import { pl } from 'date-fns/locale';

const AnalysisList = ({ chartId, onSelectAnalysis }) => {
  const navigate = useNavigate();
  const { lifeAreas } = useAppContext();
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalyses = async () => {
      try {
        setLoading(true);
        const analysesData = await analysisApi.getChartAnalyses(chartId);
        setAnalyses(analysesData);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch analyses:', err);
        setError(
          err.response?.data?.error || 'Nie udało się pobrać analiz kosmogramu.'
        );
      } finally {
        setLoading(false);
      }
    };

    fetchAnalyses();
  }, [chartId]);

  // Format date
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return format(date, "d MMMM yyyy 'o' HH:mm", { locale: pl });
    } catch (e) {
      return dateString;
    }
  };

  // Get life area name by ID
  const getLifeAreaName = (areaId) => {
    const area = lifeAreas.find((a) => a.id === areaId);
    return area ? area.name : 'Nieznany obszar';
  };

  if (loading) {
    return <Loading message="Pobieranie analiz..." />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (analyses.length === 0) {
    return (
      <Card>
        <CardContent>
          <Box sx={{ textAlign: 'center', py: 2 }}>
            <Typography variant="h6" gutterBottom>
              Brak analiz
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Ten kosmogram nie ma jeszcze wykonanych analiz.
            </Typography>
            <Button
              variant="contained"
              color="primary"
              startIcon={<AnalyticsIcon />}
              onClick={() => navigate(`/analysis/${chartId}`)}
              sx={{ mt: 2 }}
            >
              Wykonaj analizę
            </Button>
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Przeprowadzone analizy
        </Typography>
        <List disablePadding>
          {analyses.map((analysis, index) => (
            <React.Fragment key={analysis.id}>
              {index > 0 && <Divider />}
              <ListItem disablePadding>
                <ListItemButton onClick={() => onSelectAnalysis(analysis.id)}>
                  <ListItemText
                    primary={getLifeAreaName(analysis.life_area_id)}
                    secondary={formatDate(analysis.created_at)}
                  />
                  <Chip
                    label="Zobacz"
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </ListItemButton>
              </ListItem>
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default AnalysisList;
