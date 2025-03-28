/**
 * Główny plik JavaScript aplikacji
 */

/**
 * Funkcja inicjalizująca aplikację
 */
function initApp() {
    // Aktualizacja roku w stopce
    const yearElement = document.getElementById('current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
    
    // Inicjalizacja tooltipów Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Inicjalizacja popoverów Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Nasłuchiwanie na zdarzenia formularza
    setupFormValidation();
}

/**
 * Inicjalizacja walidacji formularzy
 */
function setupFormValidation() {
    // Pobierz wszystkie formularze z klasą 'needs-validation'
    const forms = document.querySelectorAll('.needs-validation');
    
    // Dodaj obsługę zdarzenia submit dla każdego formularza
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Wyświetla wiadomość o błędzie
 * @param {string} message - Treść błędu
 * @param {string} [containerId='error-alert'] - ID kontenera na komunikat błędu
 */
function showError(message, containerId = 'error-alert') {
    const container = document.getElementById(containerId);
    if (container) {
        container.textContent = message;
        container.classList.remove('d-none');
        
        // Przewiń do komunikatu błędu
        container.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
        console.error(message);
        alert(message);
    }
}

/**
 * Ukrywa komunikat o błędzie
 * @param {string} [containerId='error-alert'] - ID kontenera na komunikat błędu
 */
function hideError(containerId = 'error-alert') {
    const container = document.getElementById(containerId);
    if (container) {
        container.classList.add('d-none');
    }
}

/**
 * Wyświetla komunikat sukcesu
 * @param {string} message - Treść komunikatu
 * @param {string} [containerId='success-alert'] - ID kontenera na komunikat sukcesu
 */
function showSuccess(message, containerId = 'success-alert') {
    const container = document.getElementById(containerId);
    if (container) {
        container.textContent = message;
        container.classList.remove('d-none');
        
        // Przewiń do komunikatu sukcesu
        container.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Ukryj komunikat po 5 sekundach
        setTimeout(() => {
            container.classList.add('d-none');
        }, 5000);
    } else {
        console.log(message);
        alert(message);
    }
}

/**
 * Wyświetla loader
 * @param {string} [containerId='loader'] - ID kontenera na loader
 * @param {string} [message='Ładowanie...'] - Komunikat
 */
function showLoader(containerId = 'loader', message = 'Ładowanie...') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="text-center my-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Ładowanie...</span>
                </div>
                <p class="mt-2">${message}</p>
            </div>
        `;
        container.classList.remove('d-none');
    }
}

/**
 * Ukrywa loader
 * @param {string} [containerId='loader'] - ID kontenera na loader
 */
function hideLoader(containerId = 'loader') {
    const container = document.getElementById(containerId);
    if (container) {
        container.classList.add('d-none');
    }
}

// Uruchom inicjalizację po załadowaniu dokumentu
document.addEventListener('DOMContentLoaded', initApp);
