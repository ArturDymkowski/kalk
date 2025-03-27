import React from 'react';
import { Box, Paper, Typography } from '@mui/material';

// Znaki zodiaku w kolejności od Barana do Ryb
const zodiacSigns = [
  'Baran', 'Byk', 'Bliźnięta', 'Rak', 
  'Lew', 'Panna', 'Waga', 'Skorpion', 
  'Strzelec', 'Koziorożec', 'Wodnik', 'Ryby'
];

// Skrócone nazwy planet do wyświetlania w kosmogramie
const planetAbbreviations = {
  'Sun': 'Su',
  'Moon': 'Mo',
  'Mercury': 'Me',
  'Venus': 'Ve',
  'Mars': 'Ma',
  'Jupiter': 'Ju',
  'Saturn': 'Sa',
  'Rahu': 'Ra',
  'Ketu': 'Ke',
  'Ascendant': 'Asc'
};

// Kolory dla planet
const planetColors = {
  'Sun': '#FFA500',     // Pomarańczowy
  'Moon': '#SILVER',    // Srebrny
  'Mercury': '#32CD32', // Zielony
  'Venus': '#EE82EE',   // Fioletowy
  'Mars': '#FF0000',    // Czerwony
  'Jupiter': '#FFFF00', // Żółty
  'Saturn': '#0000FF',  // Niebieski
  'Rahu': '#800080',    // Purpurowy
  'Ketu': '#800080',    // Purpurowy
  'Ascendant': '#FF0000' // Czerwony
};

const ChartVisualization = ({ chartData, vargaType }) => {
  if (!chartData || !chartData.planets) {
    return (
      <Box sx={{ textAlign: 'center', py: 2 }}>
        <Typography variant="body2" color="text.secondary">
          Brak danych do wizualizacji kosmogramu.
        </Typography>
      </Box>
    );
  }

  // Przygotuj dane planet
  const planetsInSigns = {};
  
  // Inicjalizuj puste tablice dla każdego znaku
  zodiacSigns.forEach((sign, i) => {
    planetsInSigns[i] = [];
  });
  
  // Dodaj planety do odpowiednich znaków
  Object.entries(chartData.planets).forEach(([planet, data]) => {
    if (planetsInSigns[data.sign]) {
      planetsInSigns[data.sign].push({
        name: planet,
        abbr: planetAbbreviations[planet] || planet.substring(0, 2),
        degrees: data.degrees_in_sign,
        color: planetColors[planet] || '#000000'
      });
    }
  });

  // Style dla elementów kosmogramu
  const chartStyles = {
    chart: {
      display: 'grid',
      gridTemplateColumns: 'repeat(4, 1fr)',
      gridTemplateRows: 'repeat(3, 1fr)',
      gap: '2px',
      height: '400px',
      width: '100%',
      backgroundColor: '#f5f5f5',
      padding: '2px',
    },
    house: {
      display: 'flex',
      flexDirection: 'column',
      border: '1px solid #ccc',
      padding: '8px',
      backgroundColor: '#fff',
      height: '100%',
    },
    houseNumber: {
      fontSize: '0.75rem',
      color: '#666',
      marginBottom: '4px',
    },
    sign: {
      fontWeight: 'bold',
      marginBottom: '4px',
      fontSize: '0.9rem',
    },
    planets: {
      display: 'flex',
      flexDirection: 'column',
      gap: '2px',
      flexGrow: 1,
    },
    planet: {
      display: 'flex',
      alignItems: 'center',
      fontSize: '0.8rem',
      padding: '2px 4px',
      borderRadius: '4px',
      marginBottom: '2px',
    },
  };

  // Układ domów w siatce wedyjskiej (South Indian style)
  // Indeksy odnoszą się do znaków zodiaku (0-11)
  const houseLayout = [
    8, 9, 10, 11, // Górny rząd: Dom 9, 10, 11, 12
    7, null, null, 0, // Środkowy rząd: Dom 8, -, -, Dom 1
    6, 5, 4, 3, // Dolny rząd: Dom 7, 6, 5, 4
  ];

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom align="center">
        Kosmogram {vargaType}
      </Typography>
      
      <Box sx={chartStyles.chart}>
        {houseLayout.map((signIndex, i) => {
          if (signIndex === null) {
            // Puste miejsce w środku kosmogramu
            return <Box key={`empty-${i}`} />;
          }

          const houseNumber = (signIndex + 1) % 12 || 12; // Przekształcenie indeksu znaku na numer domu (1-12)
          const planets = planetsInSigns[signIndex] || [];
          
          return (
            <Box key={`house-${signIndex}`} sx={chartStyles.house}>
              <Typography sx={chartStyles.houseNumber}>
                Dom {houseNumber}
              </Typography>
              <Typography sx={chartStyles.sign}>
                {zodiacSigns[signIndex]}
              </Typography>
              <Box sx={chartStyles.planets}>
                {planets.map((planet) => (
                  <Box
                    key={planet.name}
                    sx={{
                      ...chartStyles.planet,
                      color: planet.color,
                      border: `1px solid ${planet.color}`,
                    }}
                  >
                    {planet.abbr} {planet.degrees.toFixed(1)}°
                  </Box>
                ))}
              </Box>
            </Box>
          );
        })}
      </Box>
      
      <Box sx={{ mt: 2, textAlign: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          Wizualizacja w stylu południowoindyjskim
        </Typography>
      </Box>
    </Paper>
  );
};

export default ChartVisualization;
