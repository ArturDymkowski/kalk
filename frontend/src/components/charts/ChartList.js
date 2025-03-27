import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
  Paper,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import ErrorMessage from '../common/ErrorMessage';
import Loading from '../common/Loading';
import { useAppContext } from '../../contexts/AppContext';
import { format } from 'date-fns';
import { pl } from 'date-fns/locale';

const ChartList = () => {
  const navigate = useNavigate();
  const { charts, loading, error, refreshCharts } = useAppContext();

  // Formatuj datę urodzenia
  const formatBirthDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return format(date, "d MMMM yyyy 'o' HH:mm", { locale: pl });
    } catch (e) {
      return dateString;
    }
  };

  if (loading) {
    return <Loading message="Pobieranie kosmogramów..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={refreshCharts} />;
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Kosmogramy
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => navigate('/charts/new')}
        >
          Nowy kosmogram
        </Button>
      </Box>

      {charts.length === 0 ? (
        <Card>
          <CardContent>
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="h6" gutterBottom>
                Brak kosmogramów
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Utwórz pierwszy kosmogram, aby rozpocząć pracę z aplikacją.
              </Typography>
              <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={() => navigate('/charts/new')}
                sx={{ mt: 2 }}
              >
                Utwórz kosmogram
              </Button>
            </Box>
          </CardContent>
        </Card>
      ) : (
        <Paper elevation={2}>
          <List disablePadding>
            {charts.map((chart, index) => (
              <React.Fragment key={chart.id}>
                {index > 0 && <Divider />}
                <ListItem
                  disablePadding
                  secondaryAction={
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<AnalyticsIcon />}
                      onClick={() => navigate(`/analysis/${chart.id}`)}
                      sx={{ mr: 1 }}
                    >
                      Analizuj
                    </Button>
                  }
                >
                  <ListItemButton onClick={() => navigate(`/charts/${chart.id}`)}>
                    <ListItemText
                      primary={chart.name}
                      secondary={
                        <Grid container spacing={1} alignItems="center">
                          <Grid item>
                            <AccessTimeIcon fontSize="small" color="action" />
                          </Grid>
                          <Grid item>{formatBirthDate(chart.birth_date)}</Grid>
                        </Grid>
                      }
                    />
                  </ListItemButton>
                </ListItem>
              </React.Fragment>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  );
};

export default ChartList;
