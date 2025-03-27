import React, { createContext, useState, useEffect } from 'react';
import { chartsApi, lifeAreasApi } from '../api/apiClient';

// Utwórz kontekst
export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  // Stan aplikacji
  const [charts, setCharts] = useState([]);
  const [lifeAreas, setLifeAreas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Pobierz dane przy pierwszym renderowaniu
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        // Pobierz kosmogramy i obszary życia równolegle
        const [chartsData, lifeAreasData] = await Promise.all([
          chartsApi.getAllCharts(),
          lifeAreasApi.getAllLifeAreas()
        ]);
        
        setCharts(chartsData);
        setLifeAreas(lifeAreasData);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch initial data:', err);
        setError('Nie udało się pobrać danych. Spróbuj odświeżyć stronę.');
      } finally {
        setLoading(false);
      }
    };

    fetchInitialData();
  }, []);

  // Funkcje do aktualizacji stanu
  const addChart = (newChart) => {
    setCharts((prevCharts) => [...prevCharts, newChart]);
  };

  const updateChart = (updatedChart) => {
    setCharts((prevCharts) =>
      prevCharts.map((chart) =>
        chart.id === updatedChart.id ? updatedChart : chart
      )
    );
  };

  const refreshCharts = async () => {
    try {
      setLoading(true);
      const chartsData = await chartsApi.getAllCharts();
      setCharts(chartsData);
    } catch (err) {
      console.error('Failed to refresh charts:', err);
      setError('Nie udało się odświeżyć kosmogramów.');
    } finally {
      setLoading(false);
    }
  };

  const refreshLifeAreas = async () => {
    try {
      setLoading(true);
      const lifeAreasData = await lifeAreasApi.getAllLifeAreas();
      setLifeAreas(lifeAreasData);
    } catch (err) {
      console.error('Failed to refresh life areas:', err);
      setError('Nie udało się odświeżyć obszarów życia.');
    } finally {
      setLoading(false);
    }
  };

  // Wartość kontekstu
  const contextValue = {
    // Dane
    charts,
    lifeAreas,
    loading,
    error,
    
    // Funkcje
    addChart,
    updateChart,
    refreshCharts,
    refreshLifeAreas,
    
    // Flagi stanu
    hasCharts: charts.length > 0,
    hasLifeAreas: lifeAreas.length > 0
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

// Hook do łatwego dostępu do kontekstu
export const useAppContext = () => {
  const context = React.useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

export default AppContext;
