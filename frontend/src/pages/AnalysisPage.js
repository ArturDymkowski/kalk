import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Grid, Box } from '@mui/material';
import AnalysisForm from '../components/analysis/AnalysisForm';
import AnalysisList from '../components/analysis/AnalysisList';
import AnalysisResult from '../components/analysis/AnalysisResult';

const AnalysisPage = () => {
  const { chartId } = useParams();
  const [selectedAnalysisId, setSelectedAnalysisId] = useState(null);

  const handleSelectAnalysis = (analysisId) => {
    setSelectedAnalysisId(analysisId);
  };

  return (
    <Container maxWidth="lg">
      <AnalysisForm />
      
      <Box sx={{ mt: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <AnalysisList 
              chartId={chartId} 
              onSelectAnalysis={handleSelectAnalysis} 
            />
          </Grid>
          <Grid item xs={12} md={8}>
            <AnalysisResult analysisId={selectedAnalysisId} />
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default AnalysisPage;
