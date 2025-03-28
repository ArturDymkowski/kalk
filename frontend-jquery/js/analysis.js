/**
 * Moduł obsługi analiz kosmogramów
 */

/**
 * Renderuje listę analiz
 * @param {string} containerId - ID kontenera HTML
 * @param {Array} analyses - Lista analiz
 * @param {Function} onSelectAnalysis - Callback wywoływany przy wyborze analizy
 */
function renderAnalysesList(containerId, analyses, onSelectAnalysis) {
    const container = document.getElementById(containerId);
    if (!container || !analyses) {
        console.error('Brak kontenera lub danych analiz');
        return;
    }
    
    // Sortuj analizy według daty (od najnowszej)
    analyses.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    let listHtml = '';
    
    analyses.forEach(analysis => {
        // Formatuj datę
        const date = new Date(analysis.created_at);
        const formattedDate = date.toLocaleDateString('pl-PL', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
        
        listHtml += `
            <a href="#" class="list-group-item list-group-item-action analysis-item" data-analysis-id="${analysis.id}">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${analysis.life_area_name}</h6>
                    <small>${formattedDate}</small>
                </div>
            </a>
        `;
    });
    
    container.innerHTML = listHtml;
    
    // Dodaj obsługę kliknięcia
    const listItems = container.querySelectorAll('.analysis-item');
    listItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Usuń klasę aktywną z wszystkich elementów
            listItems.forEach(i => i.classList.remove('active'));
            
            // Dodaj klasę aktywną do klikniętego elementu
            this.classList.add('active');
            
            const analysisId = this.getAttribute('data-analysis-id');
            if (onSelectAnalysis && typeof onSelectAnalysis === 'function') {
                onSelectAnalysis(analysisId);
            }
        });
    });
}

/**
 * Renderuje wynik analizy
 * @param {string} containerId - ID kontenera HTML
 * @param {Object} analysis - Dane analizy
 */
function renderAnalysisResult(containerId, analysis) {
    const container = document.getElementById(containerId);
    if (!container || !analysis) {
        console.error('Brak kontenera lub danych analizy');
        return;
    }
    
    // Formatuj datę
    const date = new Date(analysis.created_at);
    const formattedDate = date.toLocaleDateString('pl-PL', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    // Konwertuj tekst analizy na paragraf HTML
    const analysisContent = analysis.analysis_result
        .split('\n\n')
        .map(paragraph => paragraph.trim())
        .filter(paragraph => paragraph.length > 0)
        .map(paragraph => `<p>${paragraph}</p>`)
        .join('');
    
    const resultHtml = `
        <h5 class="card-title">Analiza: ${analysis.life_area_name}</h5>
        <div class="text-muted mb-3">Analiza wykonana: ${formattedDate}</div>
        
        <hr>
        
        <div class="analysis-content mt-3">
            ${analysisContent}
        </div>
    `;
    
    container.innerHTML = resultHtml;
}

/**
 * Wypełnia select obszarów życia
 * @param {string} selectId - ID elementu select
 * @param {Array} lifeAreas - Lista obszarów życia
 * @param {Function} onChange - Callback wywoływany przy zmianie wyboru
 */
function fillLifeAreasSelect(selectId, lifeAreas, onChange) {
    const select = document.getElementById(selectId);
    if (!select || !lifeAreas) {
        console.error('Brak elementu select lub danych obszarów życia');
        return;
    }
    
    // Wyczyść select
    select.innerHTML = '<option value="" selected disabled>Wybierz obszar życia...</option>';
    
    // Dodaj opcje obszarów życia
    lifeAreas.forEach(area => {
        const option = document.createElement('option');
        option.value = area.id;
        option.textContent = `${area.name} (${area.varga_combination})`;
        option.setAttribute('data-description', area.description || '');
        select.appendChild(option);
    });
    
    // Dodaj obsługę zmiany
    if (onChange && typeof onChange === 'function') {
        select.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const description = selectedOption.getAttribute('data-description');
            onChange(this.value, description);
        });
    }
}

/**
 * Analizuje kosmogram i wyświetla rezultat
 * @param {number} chartId - ID kosmogramu
 * @param {number} lifeAreaId - ID obszaru życia
 * @param {string} resultContainerId - ID kontenera na wynik
 * @param {Function} onComplete - Callback wywoływany po zakończeniu analizy
 */
function performAnalysis(chartId, lifeAreaId, resultContainerId, onComplete) {
    // Wyświetl spinner
    const container = document.getElementById(resultContainerId);
    if (container) {
        container.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Analizowanie...</span>
                </div>
                <p class="mt-2">Generowanie analizy kosmogramu...</p>
                <p class="text-muted small">To może potrwać do kilku minut.</p>
            </div>
        `;
    }
    
    // Wykonaj analizę
    analyzeChart(chartId, lifeAreaId)
        .then(result => {
            // Pobierz pełne dane analizy
            return getAnalysis(result.analysis_id);
        })
        .then(analysis => {
            // Renderuj wynik analizy
            renderAnalysisResult(resultContainerId, analysis);
            
            // Wywołaj callback
            if (onComplete && typeof onComplete === 'function') {
                onComplete(analysis);
            }
        })
        .catch(error => {
            console.error('Analysis failed:', error);
            
            // Wyświetl błąd
            if (container) {
                container.innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        <h5 class="alert-heading">Błąd analizy</h5>
                        <p>${error.message || 'Nie udało się przeprowadzić analizy. Spróbuj ponownie.'}</p>
                    </div>
                `;
            }
            
            // Wywołaj callback z błędem
            if (onComplete && typeof onComplete === 'function') {
                onComplete(null, error);
            }
        });
}
