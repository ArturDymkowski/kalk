import axios from 'axios';

// Utwórz instancję axios z podstawową konfiguracją
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptory do obsługi błędów
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Centralna obsługa błędów
    console.error('API Error:', error.response || error.message);
    return Promise.reject(error);
  }
);

// API kosmogramów
const chartsApi = {
  // Pobierz wszystkie kosmogramy
  getAllCharts: async () => {
    const response = await apiClient.get('/charts');
    return response.data.charts;
  },
  
  // Pobierz szczegóły kosmogramu
  getChart: async (chartId) => {
    const response = await apiClient.get(`/chart/${chartId}`);
    return response.data;
  },
  
  // Utwórz nowy kosmogram
  createChart: async (chartData) => {
    const response = await apiClient.post('/chart', chartData);
    return response.data;
  }
};

// API obszarów życia
const lifeAreasApi = {
  // Pobierz wszystkie obszary życia
  getAllLifeAreas: async () => {
    const response = await apiClient.get('/life-areas');
    return response.data.life_areas;
  },
  
  // Pobierz szczegóły obszaru życia
  getLifeArea: async (areaId) => {
    const response = await apiClient.get(`/life-area/${areaId}`);
    return response.data;
  },
  
  // Zaktualizuj prompt dla obszaru życia
  updateLifeAreaPrompt: async (areaId, promptTemplate) => {
    const response = await apiClient.put(`/life-area/${areaId}`, {
      prompt_template: promptTemplate
    });
    return response.data;
  }
};

// API analiz
const analysisApi = {
  // Przeprowadź analizę kosmogramu
  analyzeChart: async (chartId, lifeAreaId) => {
    const response = await apiClient.post('/analyze', {
      chart_id: chartId,
      life_area_id: lifeAreaId
    });
    return response.data;
  },
  
  // Pobierz wszystkie analizy dla kosmogramu
  getChartAnalyses: async (chartId) => {
    const response = await apiClient.get(`/analyses/${chartId}`);
    return response.data.analyses;
  },
  
  // Pobierz szczegóły analizy
  getAnalysis: async (analysisId) => {
    const response = await apiClient.get(`/analysis/${analysisId}`);
    return response.data;
  }
};

// Eksportuj wszystkie API
export { chartsApi, lifeAreasApi, analysisApi };

// Eksportuj domyślnie cały klient API
export default apiClient;
