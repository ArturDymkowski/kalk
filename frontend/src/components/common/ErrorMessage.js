import React from 'react';
import { Alert, AlertTitle, Box, Button } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

const ErrorMessage = ({ 
  message = 'Wystąpił błąd. Spróbuj ponownie później.', 
  severity = 'error',
  onRetry = null
}) => {
  return (
    <Box sx={{ my: 2 }}>
      <Alert 
        severity={severity}
        action={
          onRetry && (
            <Button 
              color="inherit" 
              size="small"
              startIcon={<RefreshIcon />}
              onClick={onRetry}
            >
              Spróbuj ponownie
            </Button>
          )
        }
      >
        <AlertTitle>Błąd</AlertTitle>
        {message}
      </Alert>
    </Box>
  );
};

export default ErrorMessage;
