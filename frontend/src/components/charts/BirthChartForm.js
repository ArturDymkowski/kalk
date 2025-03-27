import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardActions,
  TextField,
  Typography,
  Grid,
  Divider,
  Alert,
} from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { chartsApi } from '../../api/apiClient';
import { useAppContext } from '../../contexts/AppContext';
import Loading from '../common/Loading';

const BirthChartForm = () => {
  const navigate = useNavigate();
  const { addChart, refreshCharts } = useAppContext();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      name: '',
      birth_date: new Date(),
      latitude: '',
      longitude: '',
    },
  });

  const onSubmit = async (data) => {
    try {
      setLoading(true);
      setError(null);

      // Format date to ISO string
      const formattedData = {
        ...data,
        birth_date: data.birth_date.toISOString(),
        latitude: parseFloat(data.latitude),
        longitude: parseFloat(data.longitude),
      };

      // Send data to API
      const response = await chartsApi.createChart(formattedData);

      // Update context
      await refreshCharts();

      // Redirect to chart detail page
      navigate(`/charts/${response.chart_id}`);
    } catch (err) {
      console.error('Failed to create chart:', err);
      setError(
        err.response?.data?.error || 'Nie udało się utworzyć kosmogramu. Spróbuj ponownie.'
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading message="Tworzenie kosmogramu..." />;
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h2" gutterBottom>
          Nowy kosmogram
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Wprowadź dane do utworzenia kosmogramu astrologicznego.
        </Typography>

        <Divider sx={{ my: 2 }} />

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" noValidate onSubmit={handleSubmit(onSubmit)} sx={{ mt: 2 }}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Controller
                name="name"
                control={control}
                rules={{ required: 'Imię i nazwisko jest wymagane' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Imię i nazwisko"
                    fullWidth
                    variant="outlined"
                    error={!!errors.name}
                    helperText={errors.name?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="birth_date"
                control={control}
                rules={{ required: 'Data urodzenia jest wymagana' }}
                render={({ field }) => (
                  <DateTimePicker
                    {...field}
                    label="Data i godzina urodzenia"
                    ampm={false}
                    format="dd.MM.yyyy HH:mm"
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        variant: 'outlined',
                        error: !!errors.birth_date,
                        helperText: errors.birth_date?.message,
                      },
                    }}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="latitude"
                control={control}
                rules={{
                  required: 'Szerokość geograficzna jest wymagana',
                  pattern: {
                    value: /^-?([0-8]?[0-9]|90)(\.[0-9]{1,6})?$/,
                    message: 'Niepoprawny format (np. 50.0413)',
                  },
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Szerokość geograficzna"
                    fullWidth
                    variant="outlined"
                    placeholder="np. 50.0413"
                    error={!!errors.latitude}
                    helperText={errors.latitude?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="longitude"
                control={control}
                rules={{
                  required: 'Długość geograficzna jest wymagana',
                  pattern: {
                    value: /^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,6})?$/,
                    message: 'Niepoprawny format (np. 19.9738)',
                  },
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Długość geograficzna"
                    fullWidth
                    variant="outlined"
                    placeholder="np. 19.9738"
                    error={!!errors.longitude}
                    helperText={errors.longitude?.message}
                  />
                )}
              />
            </Grid>
          </Grid>
        </Box>
      </CardContent>
      <CardActions sx={{ px: 2, pb: 2 }}>
        <Button 
          variant="outlined" 
          onClick={() => navigate('/charts')}
          sx={{ mr: 1 }}
        >
          Anuluj
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit(onSubmit)}
          disabled={loading}
        >
          Utwórz kosmogram
        </Button>
      </CardActions>
    </Card>
  );
};

export default BirthChartForm;
