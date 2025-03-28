/**
 * Moduł obsługi kosmogramów
 */

/**
 * Renderuje wizualizację kosmogramu w stylu południowoindyjskim
 * @param {string} containerId - ID kontenera HTML
 * @param {Object} chartData - Dane kosmogramu
 */
function renderVedicChart(containerId, chartData) {
    const container = document.getElementById(containerId);
    if (!container || !chartData || !chartData.planets) {
        console.error('Brak kontenera lub danych do wizualizacji kosmogramu');
        return;
    }
    
    // Znaki zodiaku w kolejności od Barana do Ryb
    const zodiacSigns = [
        'Baran', 'Byk', 'Bliźnięta', 'Rak', 
        'Lew', 'Panna', 'Waga', 'Skorpion', 
        'Strzelec', 'Koziorożec', 'Wodnik', 'Ryby'
    ];
    
    // Przygotuj dane planet
    const planetsInSigns = {};
    
    // Inicjalizuj puste tablice dla każdego znaku
    zodiacSigns.forEach((sign, i) => {
        planetsInSigns[i] = [];
    });
    
    // Skrócone nazwy planet do wyświetlania w kosmogramie
    const planetAbbreviations = {
        'Ascendant': 'Asc',
        'Sun': 'Su',
        'Moon': 'Mo',
        'Mercury': 'Me',
        'Venus': 'Ve',
        'Mars': 'Ma',
        'Jupiter': 'Ju',
        'Saturn': 'Sa',
        'Rahu': 'Ra',
        'Ketu': 'Ke'
    };
    
    // Dodaj planety do odpowiednich znaków
    Object.entries(chartData.planets).forEach(([planet, data]) => {
        if (planetsInSigns[data.sign] !== undefined) {
            planetsInSigns[data.sign].push({
                name: planet,
                abbr: planetAbbreviations[planet] || planet.substring(0, 2),
                degrees: data.degrees_in_sign
            });
        }
    });
    
    // Układ domów w siatce południowoindyjskiej (South Indian style)
    // Indeksy odnoszą się do znaków zodiaku (0-11)
    const houseLayout = [
        8, 9, 10, 11, // Górny rząd: Dom 9, 10, 11, 12
        7, null, null, 0, // Środkowy rząd: Dom 8, -, -, Dom 1
        6, 5, 4, 3, // Dolny rząd: Dom 7, 6, 5, 4
    ];
    
    // Tworzenie wizualizacji kosmogramu
    let chartHtml = '<div class="vedic-chart">';
    
    // Iteruj po układzie domów
    houseLayout.forEach((signIndex, i) => {
        if (signIndex === null) {
            // Puste miejsce w środku kosmogramu
            chartHtml += '<div class="chart-cell chart-cell-empty"></div>';
        } else {
            const houseNumber = (signIndex + 1) % 12 || 12; // Przekształcenie indeksu znaku na numer domu (1-12)
            const planets = planetsInSigns[signIndex] || [];
            
            chartHtml += `
                <div class="chart-cell">
                    <div class="chart-cell-content">
                        <div class="chart-house-number">Dom ${houseNumber}</div>
                        <div class="chart-sign">${zodiacSigns[signIndex]}</div>
                        <div class="chart-planets">
            `;
            
            // Dodaj planety
            planets.forEach(planet => {
                chartHtml += `
                    <div class="chart-planet planet-${planet.name.toLowerCase()}">
                        ${planet.abbr} ${planet.degrees.toFixed(1)}°
                    </div>
                `;
            });
            
            chartHtml += `
                        </div>
                    </div>
                </div>
            `;
        }
    });
    
    chartHtml += '</div>';
    
    // Dodaj legendę
    chartHtml += `
        <div class="chart-info mt-2 text-center">
            <small class="text-muted">Wizualizacja w stylu południowoindyjskim</small>
        </div>
    `;
    
    container.innerHTML = chartHtml;
}

/**
 * Renderuje tabelę planet z kosmogramu
 * @param {string} containerId - ID kontenera HTML
 * @param {Object} planets - Dane planet
 */
function renderPlanetsTable(containerId, planets) {
    const container = document.getElementById(containerId);
    if (!container || !planets) {
        console.error('Brak kontenera lub danych planet');
        return;
    }
    
    // Sortuj planety w określonej kolejności
    const planetOrder = [
        'Ascendant', 'Sun', 'Moon', 'Mercury', 
        'Venus', 'Mars', 'Jupiter', 'Saturn', 
        'Rahu', 'Ketu'
    ];
    
    // Planety po polsku
    const planetNames = {
        'Ascendant': 'Ascendent',
        'Sun': 'Słońce',
        'Moon': 'Księżyc',
        'Mercury': 'Merkury',
        'Venus': 'Wenus',
        'Mars': 'Mars',
        'Jupiter': 'Jowisz',
        'Saturn': 'Saturn',
        'Rahu': 'Rahu',
        'Ketu': 'Ketu'
    };
    
    let tableHtml = `
        <table class="table table-sm table-hover">
            <thead>
                <tr>
                    <th>Planeta</th>
                    <th>Znak</th>
                    <th>Pozycja</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    // Iteruj po planetach w określonej kolejności
    planetOrder.forEach(planetKey => {
        if (planets[planetKey]) {
            const planet = planets[planetKey];
            tableHtml += `
                <tr>
                    <td>
                        <span class="planet-icon planet-${planetKey.toLowerCase()}"></span>
                        ${planetNames[planetKey] || planetKey}
                    </td>
                    <td>${planet.sign_name}</td>
                    <td>${planet.degrees_in_sign.toFixed(2)}°</td>
                </tr>
            `;
        }
    });
    
    tableHtml += `
            </tbody>
        </table>
    `;
    
    container.innerHTML = tableHtml;
}

/**
 * Renderuje zakładki dla różnych varg kosmogramu
 * @param {string} tabsContainerId - ID kontenera zakładek
 * @param {string} contentContainerId - ID kontenera treści zakładek
 * @param {Object} chartData - Dane kosmogramu
 * @param {Function} onTabChange - Callback wywoływany przy zmianie zakładki
 */
function renderVargaTabs(tabsContainerId, contentContainerId, chartData, onTabChange) {
    const tabsContainer = document.getElementById(tabsContainerId);
    const contentContainer = document.getElementById(contentContainerId);
    
    if (!tabsContainer || !contentContainer || !chartData) {
        console.error('Brak kontenerów lub danych kosmogramu');
        return;
    }
    
    const vargaTabs = [
        { id: 'D1', label: 'D1 - Rashi', description: 'Główna mapa życia' },
        { id: 'D2', label: 'D2 - Hora', description: 'Bogactwo i finanse' },
        { id: 'D3', label: 'D3 - Drekkana', description: 'Rodzeństwo i motywacja' },
        { id: 'D4', label: 'D4 - Chaturtamsa', description: 'Nieruchomości i luksus' },
        { id: 'D5', label: 'D5 - Panchamsa', description: 'Kreatywność i zasługi' },
        { id: 'D6', label: 'D6 - Shashtamsa', description: 'Zdrowie i choroby' },
        { id: 'D7', label: 'D7 - Saptamsa', description: 'Dzieci i płodność' },
        { id: 'D8', label: 'D8 - Ashtamsa', description: 'Nagłe zmiany, transformacje' },
        { id: 'D9', label: 'D9 - Navamsa', description: 'Związki i dharma' },
        { id: 'D10', label: 'D10 - Dasamsa', description: 'Kariera i sukces zawodowy' },
        { id: 'D11', label: 'D11 - Ekadasamsa', description: 'Przyjaciele i zyski' },
        { id: 'D12', label: 'D12 - Dvadasamsa', description: 'Rodzice i karma rodowa' }
    ];
    
    // Generuj zakładki
    let tabsHtml = '<ul class="nav nav-tabs" role="tablist">';
    
    vargaTabs.forEach((varga, index) => {
        tabsHtml += `
            <li class="nav-item" role="presentation">
                <button class="nav-link ${index === 0 ? 'active' : ''}" 
                    id="tab-${varga.id}" 
                    data-bs-toggle="tab" 
                    data-bs-target="#content-${varga.id}" 
                    type="button" 
                    role="tab" 
                    data-varga="${varga.id}"
                    aria-controls="content-${varga.id}" 
                    aria-selected="${index === 0 ? 'true' : 'false'}">
                    ${varga.label}
                </button>
            </li>
        `;
    });
    
    tabsHtml += '</ul>';
    tabsContainer.innerHTML = tabsHtml;
    
    // Generuj zawartość zakładek
    let contentHtml = '<div class="tab-content">';
    
    vargaTabs.forEach((varga, index) => {
        // Sprawdź czy dane vargi są dostępne
        const vargaData = chartData.vargas && chartData.vargas[varga.id];
        
        if (vargaData) {
            contentHtml += `
                <div class="tab-pane fade ${index === 0 ? 'show active' : ''}" 
                    id="content-${varga.id}" 
                    role="tabpanel" 
                    aria-labelledby="tab-${varga.id}">
                    
                    <div class="mb-3">
                        <h5>${varga.label}</h5>
                        <p class="text-muted">${varga.description}</p>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div id="chart-${varga.id}"></div>
                        </div>
                        <div class="col-md-6">
                            <h6 class="mb-3">Pozycje planet</h6>
                            <div id="planets-${varga.id}"></div>
                        </div>
                    </div>
                </div>
            `;
        } else {
            contentHtml += `
                <div class="tab-pane fade ${index === 0 ? 'show active' : ''}" 
                    id="content-${varga.id}" 
                    role="tabpanel" 
                    aria-labelledby="tab-${varga.id}">
                    
                    <div class="text-center py-4">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Ładowanie...</span>
                        </div>
                        <p class="mt-2">Ładowanie danych vargi...</p>
                    </div>
                </div>
            `;
        }
    });
    
    contentHtml += '</div>';
    contentContainer.innerHTML = contentHtml;
    
    // Renderuj wizualizacje dla dostępnych varg
    vargaTabs.forEach(varga => {
        const vargaData = chartData.vargas && chartData.vargas[varga.id];
        if (vargaData) {
            renderVedicChart(`chart-${varga.id}`, vargaData);
            renderPlanetsTable(`planets-${varga.id}`, vargaData.planets);
        }
    });
    
    // Obsługa zmiany zakładki
    const tabButtons = tabsContainer.querySelectorAll('button[data-bs-toggle="tab"]');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const vargaId = this.getAttribute('data-varga');
            if (onTabChange && typeof onTabChange === 'function') {
                onTabChange(vargaId);
            }
        });
    });
}
