import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { pl } from 'date-fns/locale';

// Kontekst
import { AppProvider } from './contexts/AppContext';

// Komponenty
import Header from './components/common/Header';
import Footer from './components/common/Footer';

// Strony
import HomePage from './pages/HomePage';
import ChartFormPage from './pages/ChartFormPage';
import ChartListPage from './pages/ChartListPage';
import ChartDetailPage from './pages/ChartDetailPage';
import AnalysisPage from './pages/AnalysisPage';
import NotFoundPage from './pages/NotFoundPage';

// Stworzenie motywu aplikacji
const theme = createTheme({
  palette: {
    primary: {
      main: '#673ab7', // Fioletowy kolor dla astrologii
    },
    secondary: {
      main: '#ff9800', // Pomarańczowy dla akcentów
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={pl}>
        <AppProvider>
          <Router>
            <div className="app">
              <Header />
              <main className="content">
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/charts/new" element={<ChartFormPage />} />
                  <Route path="/charts" element={<ChartListPage />} />
                  <Route path="/charts/:id" element={<ChartDetailPage />} />
                  <Route path="/analysis/:chartId" element={<AnalysisPage />} />
                  <Route path="*" element={<NotFoundPage />} />
                </Routes>
              </main>
              <Footer />
            </div>
          </Router>
        </AppProvider>
      </LocalizationProvider>
    </ThemeProvider>
  );
}

export default App;
