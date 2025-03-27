import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Divider,
  Typography,
  CircularProgress,
} from '@mui/material';
import { analysisApi } from '../../api/apiClient';
import ErrorMessage from '../common/ErrorMessage';
import { format } from 'date-fns';
import { pl } from 'date-fns/locale';

const AnalysisResult = ({ analysisId }) => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      if (!analysisId) return;
      
      try {
        setLoading(true);
        const analysisData = await analysisApi.getAnalysis(analysisId);
        setAnalysis(analysisData);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch analysis:', err);
        setError(
          err.response?.data?.error || 'Nie udało się pobrać wyników analizy.'
        );
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [analysisId]);

  // Format date
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return format(date, "d MMMM yyyy 'o' HH:mm", { locale: pl });
    } catch (e) {
      return dateString;
    }
  };

  if (!analysisId) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography variant="body2" color="text.secondary">
          Wybierz analizę z listy lub wykonaj nową analizę kosmogramu.
        </Typography>
      </Box>
    );
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!analysis) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography variant="body2" color="text.secondary">
          Nie znaleziono wybranej analizy.
        </Typography>
      </Box>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          {analysis.life_area_name}
        </Typography>
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          Analiza wykonana: {formatDate(analysis.created_at)}
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
  );
};

export default AnalysisResult;
