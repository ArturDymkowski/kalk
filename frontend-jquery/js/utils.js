/**
 * Moduł narzędzi pomocniczych
 */

/**
 * Formatuje datę do postaci "DD MMMM YYYY o HH:MM" (np. "1 stycznia 2023 o 15:30")
 * @param {string} dateString - Data w formacie ISO
 * @returns {string} Sformatowana data
 */
function formatDateTime(dateString) {
    try {
        const date = new Date(dateString);
        
        // Tablica miesięcy w języku polskim
        const months = [
            'stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca',
            'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia'
        ];
        
        const day = date.getDate();
        const month = months[date.getMonth()];
        const year = date.getFullYear();
        
        // Godzina i minuty z wiodącym zerem
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        
        return `${day} ${month} ${year} o ${hours}:${minutes}`;
    } catch (error) {
        console.error('Error formatting date:', error);
        return dateString;
    }
}

/**
 * Formatuje współrzędne geograficzne
 * @param {number} value - Wartość współrzędnej
 * @param {string} type - Typ współrzędnej ('lat' dla szerokości, 'lng' dla długości)
 * @returns {string} Sformatowana współrzędna
 */
function formatCoordinate(value, type) {
    const isNegative = value < 0;
    const absValue = Math.abs(value);
    
    const degrees = Math.floor(absValue);
    const minutes = Math.floor((absValue - degrees) * 60);
    const seconds = Math.floor(((absValue - degrees) * 60 - minutes) * 60);
    
    let direction = '';
    if (type === 'lat') {
        direction = isNegative ? 'S' : 'N';
    } else if (type === 'lng') {
        direction = isNegative ? 'W' : 'E';
    }
    
    return `${degrees}° ${minutes}' ${seconds}" ${direction}`;
}

/**
 * Generuje losowy identyfikator
 * @param {number} [length=8] - Długość identyfikatora
 * @returns {string} Losowy identyfikator
 */
function generateRandomId(length = 8) {
    const chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars[Math.floor(Math.random() * chars.length)];
    }
    return result;
}

/**
 * Pobiera parametry z adresu URL
 * @returns {Object} Obiekt z parametrami URL
 */
function getUrlParams() {
    const params = {};
    const queryString = window.location.search.substring(1);
    const pairs = queryString.split('&');
    
    for (let i = 0; i < pairs.length; i++) {
        const pair = pairs[i].split('=');
        params[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1] || '');
    }
    
    return params;
}

/**
 * Tworzy ciąg zapytania z obiektu
 * @param {Object} params - Obiekt z parametrami
 * @returns {string} Ciąg zapytania (np. "?key1=value1&key2=value2")
 */
function buildQueryString(params) {
    if (!params || Object.keys(params).length === 0) {
        return '';
    }
    
    const parts = [];
    
    for (const key in params) {
        if (params.hasOwnProperty(key) && params[key] !== undefined && params[key] !== null) {
            parts.push(encodeURIComponent(key) + '=' + encodeURIComponent(params[key]));
        }
    }
    
    return '?' + parts.join('&');
}

/**
 * Przechodzi do strony z parametrami
 * @param {string} url - URL bazowy
 * @param {Object} params - Obiekt z parametrami
 */
function navigateTo(url, params) {
    window.location.href = url + buildQueryString(params);
}

/**
 * Konwertuje tekst z nowych linii na kod HTML z paragrafami
 * @param {string} text - Tekst z nowymi liniami
 * @returns {string} Kod HTML z paragrafami
 */
function textToHtml(text) {
    if (!text) return '';
    
    return text
        .split('\n\n')
        .map(paragraph => paragraph.trim())
        .filter(paragraph => paragraph.length > 0)
        .map(paragraph => `<p>${paragraph}</p>`)
        .join('');
}

/**
 * Truncate text to a certain length and add ellipsis
 * @param {string} text - Text to truncate
 * @param {number} [length=100] - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, length = 100) {
    if (!text) return '';
    if (text.length <= length) return text;
    
    return text.substring(0, length) + '...';
}
