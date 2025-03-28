/**
 * Moduł API - funkcje do komunikacji z backendem
 */

// Bazowy URL API
const API_BASE_URL = 'https://instytutastrologii/api';

/**
 * Funkcja pomocnicza do wykonywania żądań HTTP
 * @param {string} endpoint - Endpoint API
 * @param {string} method - Metoda HTTP (GET, POST, PUT, DELETE)
 * @param {Object} [data] - Dane do wysłania (dla POST i PUT)
 * @returns {Promise} Promise z odpowiedzią
 */
function apiRequest(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || `Błąd HTTP: ${response.status}`);
                });
            }
            return response.json();
        });
}

/**
 * Pobiera listę wszystkich kosmogramów
 * @returns {Promise<Array>} Promise z listą kosmogramów
 */
function getCharts() {
    return apiRequest('/charts')
        .then(data => data.charts || []);
}

/**
 * Pobiera szczegóły kosmogramu
 * @param {number|string} chartId - ID kosmogramu
 * @returns {Promise<Object>} Promise z danymi kosmogramu
 */
function getChart(chartId) {
    return apiRequest(`/chart/${chartId}`);
}

/**
 * Tworzy nowy kosmogram
 * @param {Object} chartData - Dane kosmogramu
 * @returns {Promise<Object>} Promise z odpowiedzią
 */
function createChart(chartData) {
    return apiRequest('/chart', 'POST', chartData);
}

/**
 * Pobiera listę obszarów życia
 * @returns {Promise<Array>} Promise z listą obszarów życia
 */
function getLifeAreas() {
    return apiRequest('/life-areas')
        .then(data => data.life_areas || []);
}

/**
 * Pobiera szczegóły obszaru życia
 * @param {number|string} areaId - ID obszaru życia
 * @returns {Promise<Object>} Promise z danymi obszaru życia
 */
function getLifeArea(areaId) {
    return apiRequest(`/life-area/${areaId}`);
}

/**
 * Analizuje kosmogram dla wybranego obszaru życia
 * @param {number|string} chartId - ID kosmogramu
 * @param {number|string} lifeAreaId - ID obszaru życia
 * @returns {Promise<Object>} Promise z wynikiem analizy
 */
function analyzeChart(chartId, lifeAreaId) {
    return apiRequest('/analyze', 'POST', {
        chart_id: parseInt(chartId),
        life_area_id: parseInt(lifeAreaId)
    });
}

/**
 * Pobiera analizy dla kosmogramu
 * @param {number|string} chartId - ID kosmogramu
 * @returns {Promise<Array>} Promise z listą analiz
 */
function getChartAnalyses(chartId) {
    return apiRequest(`/analyses/${chartId}`)
        .then(data => data.analyses || []);
}

/**
 * Pobiera szczegóły analizy
 * @param {number|string} analysisId - ID analizy
 * @returns {Promise<Object>} Promise z danymi analizy
 */
function getAnalysis(analysisId) {
    return apiRequest(`/analysis/${analysisId}`);
}
