from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import logging
from ..database.models import db
from ..database.utils import (
    save_birth_chart, save_varga_chart, save_chart_analysis,
    get_birth_charts, get_birth_chart, get_varga_charts,
    get_life_areas, get_life_area, get_chart_analyses
)
from ..astro.calculator import VedicAstroCalculator
from .openai_client import OpenAIClient

# Utwórz blueprint dla API
api_bp = Blueprint('api', __name__)

# Konfiguracja logowania
logger = logging.getLogger(__name__)

# Inicjalizuj kalkulator astrologiczny
calculator = VedicAstroCalculator()

# Inicjalizuj klienta OpenAI
openai_client = OpenAIClient()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Prosta trasa do sprawdzenia stanu API."""
    return jsonify({"status": "ok", "message": "API działa poprawnie"})

@api_bp.route('/chart', methods=['POST'])
def create_chart():
    """
    Tworzy nowy kosmogram na podstawie danych urodzeniowych.
    
    Wymagane dane JSON:
    {
        "name": "Imię i nazwisko",
        "birth_date": "YYYY-MM-DDTHH:MM:SS",
        "latitude": 50.123,
        "longitude": 19.456
    }
    """
    try:
        data = request.json
        
        # Walidacja danych
        if not all(key in data for key in ['name', 'birth_date', 'latitude', 'longitude']):
            return jsonify({"error": "Brakujące wymagane pola"}), 400
        
        # Parsuj datę urodzenia
        try:
            birth_date = datetime.fromisoformat(data['birth_date'])
        except ValueError:
            return jsonify({"error": "Nieprawidłowy format daty. Użyj formatu ISO (YYYY-MM-DDTHH:MM:SS)"}), 400
        
        # Zapisz kosmogram w bazie danych
        birth_chart = save_birth_chart(
            name=data['name'],
            birth_date=birth_date,
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            user_id=data.get('user_id')
        )
        
        if not birth_chart:
            return jsonify({"error": "Nie udało się zapisać kosmogramu"}), 500
        
        # Oblicz wszystkie vargi
        try:
            vargas = calculator.calculate_all_vargas(
                birth_date=birth_date,
                latitude=float(data['latitude']),
                longitude=float(data['longitude'])
            )
            
            # Zapisz vargi w bazie danych
            for varga_type, varga_data in vargas.items():
                save_varga_chart(birth_chart.id, varga_type, varga_data)
                
            return jsonify({
                "success": True,
                "message": "Kosmogram utworzony pomyślnie",
                "chart_id": birth_chart.id
            }), 201
                
        except Exception as e:
            logger.error(f"Błąd podczas obliczania varg: {str(e)}")
            return jsonify({"error": f"Nie udało się obliczyć kosmogramu: {str(e)}"}), 500
            
    except Exception as e:
        logger.error(f"Błąd podczas tworzenia kosmogramu: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/charts', methods=['GET'])
def list_charts():
    """Pobiera listę wszystkich kosmogramów."""
    try:
        charts = get_birth_charts()
        
        # Konwertuj wyniki do JSON
        charts_data = []
        for chart in charts:
            charts_data.append({
                "id": chart.id,
                "name": chart.name,
                "birth_date": chart.birth_date.isoformat(),
                "latitude": chart.latitude,
                "longitude": chart.longitude,
                "created_at": chart.created_at.isoformat()
            })
            
        return jsonify({"charts": charts_data}), 200
        
    except Exception as e:
        logger.error(f"Błąd podczas pobierania kosmogramów: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/chart/<int:chart_id>', methods=['GET'])
def get_chart(chart_id):
    """
    Pobiera szczegóły kosmogramu.
    
    Args:
        chart_id (int): ID kosmogramu
    """
    try:
        chart = get_birth_chart(chart_id)
        
        if not chart:
            return jsonify({"error": "Nie znaleziono kosmogramu"}), 404
            
        # Pobierz vargi dla tego kosmogramu
        vargas = get_varga_charts(chart_id)
        
        vargas_data = {}
        for varga_type, varga in vargas.items():
            vargas_data[varga_type] = varga.data  # Używa właściwości data z modelu VargaChart
        
        # Przygotuj dane kosmogramu
        chart_data = {
            "id": chart.id,
            "name": chart.name,
            "birth_date": chart.birth_date.isoformat(),
            "latitude": chart.latitude,
            "longitude": chart.longitude,
            "created_at": chart.created_at.isoformat(),
            "vargas": vargas_data
        }
        
        return jsonify(chart_data), 200
        
    except Exception as e:
        logger.error(f"Błąd podczas pobierania kosmogramu: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/life-areas', methods=['GET'])
def list_life_areas():
    """Pobiera listę wszystkich obszarów życia."""
    try:
        areas = get_life_areas()
        
        # Konwertuj wyniki do JSON
        areas_data = []
        for area in areas:
            areas_data.append({
                "id": area.id,
                "name": area.name,
                "description": area.description,
                "varga_combination": area.varga_combination
            })
            
        return jsonify({"life_areas": areas_data}), 200
        
    except Exception as e:
        logger.error(f"Błąd podczas pobierania obszarów życia: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/life-area/<int:area_id>', methods=['GET'])
def get_area(area_id):
    """
    Pobiera szczegóły obszaru życia.
    
    Args:
        area_id (int): ID obszaru życia
    """
    try:
        area = get_life_area(area_id)
        
        if not area:
            return jsonify({"error": "Nie znaleziono obszaru życia"}), 404
            
        # Przygotuj dane obszaru
        area_data = {
            "id": area.id,
            "name": area.name,
            "description": area.description,
            "varga_combination": area.varga_combination,
            "prompt_template": area.prompt_template
        }
        
        return jsonify(area_data), 200
        
    except Exception as e:
        logger.error(f"Błąd podczas pobierania obszaru życia: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/life-area/<int:area_id>', methods=['PUT'])
def update_area(area_id):
    """
    Aktualizuje prompt do obszaru życia.
    
    Args:
        area_id (int): ID obszaru życia
        
    Wymagane dane JSON:
    {
        "prompt_template": "Nowy szablon promptu..."
    }
    """
    try:
        data = request.json
        
        if 'prompt_template' not in data:
            return jsonify({"error": "Brakujący szablon promptu"}), 400
            
        area = get_life_area(area_id)
        
        if not area:
            return jsonify({"error": "Nie znaleziono obszaru życia"}), 404
            
        # Aktualizuj prompt
        area.prompt_template = data['prompt_template']
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Prompt zaktualizowany pomyślnie"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Błąd podczas aktualizacji obszaru życia: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/analyze', methods=['POST'])
def analyze_chart():
    """
    Analizuje kosmogram dla określonego obszaru życia.
    
    Wymagane dane JSON:
    {
        "chart_id": 1,
        "life_area_id": 1
    }
    """
    try:
        data = request.json
        
        # Walidacja danych
        if not all(key in data for key in ['chart_id', 'life_area_id']):
            return jsonify({"error": "Brakujące wymagane pola"}), 400
            
        chart_id = data['chart_id']
        life_area_id = data['life_area_id']
        
        # Pobierz kosmogram i obszar życia
        chart = get_birth_chart(chart_id)
        life_area = get_life_area(life_area_id)
        
        if not chart:
            return jsonify({"error": "Nie znaleziono kosmogramu"}), 404
            
        if not life_area:
            return jsonify({"error": "Nie znaleziono obszaru życia"}), 404
            
        # Pobierz vargi dla kosmogramu
        vargas = get_varga_charts(chart_id)
        
        # Przygotuj dane do analizy
        from ..astro.utils import combine_varga_charts
        
        # Pobierz listę varg do analizy
        varga_types = life_area.varga_combination.split(',')
        
        # Konwertuj słownik obiektów VargaChart na słownik danych
        vargas_data = {}
        for varga_type, varga in vargas.items():
            vargas_data[varga_type] = varga.data
        
        # Połącz kosmogramy varg
        combined_chart = combine_varga_charts(vargas_data, varga_types)
        
        if not combined_chart:
            return jsonify({"error": "Nie można połączyć kosmogramów varg"}), 500
            
        # Analizuj kosmogram za pomocą OpenAI
        analysis_result = openai_client.analyze_area(combined_chart, {
            'name': life_area.name,
            'description': life_area.description,
            'varga_combination': life_area.varga_combination,
            'prompt_template': life_area.prompt_template
        })
        
        if not analysis_result:
            return jsonify({"error": "Nie udało się przeprowadzić analizy"}), 500
            
        # Zapisz wynik analizy
        saved_analysis = save_chart_analysis(chart_id, life_area_id, analysis_result)
        
        if not saved_analysis:
            return jsonify({"error": "Nie udało się zapisać analizy"}), 500
            
        return jsonify({
            "success": True,
            "analysis_id": saved_analysis.id,
            "analysis_result": analysis_result
        }), 200
        
    except Exception as e:
        logger.error(f"Błąd podczas analizy kosmogramu: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/analyses/<int:chart_id>', methods=['GET'])
def list_analyses(chart_id):
    """
    Pobiera listę wszystkich analiz dla danego kosmogramu.
    
    Args:
        chart_id (int): ID kosmogramu
    """
    try:
        analyses = get_chart_analyses(chart_id)
        
        # Konwertuj wyniki do JSON
        analyses_data = []
        for analysis in analyses:
            analyses_data.append({
                "id": analysis.id,
                "chart_id": analysis.birth_chart_id,
                "life_area_id": analysis.life_area_id,
                "life_area_name": analysis.life_area.name,
                "created_at": analysis.created_at.isoformat()
            })
            
        return jsonify({"analyses": analyses_data}), 200
        
    except Exception as e:
        logger.error(f"Błąd podczas pobierania analiz: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """
    Pobiera szczegóły analizy.
    
    Args:
        analysis_id (int): ID analizy
    """
    try:
        from ..database.utils import get_chart_analysis
        
        analysis = get_chart_analysis(analysis_id)
        
        if not analysis:
            return jsonify({"error": "Nie znaleziono analizy"}), 404
            
        # Przygotuj dane analizy
        analysis_data = {
            "id": analysis.id,
            "chart_id": analysis.birth_chart_id,
            "chart_name": analysis.birth_chart.name,
            "life_area_id": analysis.life_area_id,
            "life_area_name": analysis.life_area.name,
            "analysis_result": analysis.analysis_result,
            "created_at": analysis.created_at.isoformat()
        }
        
        return jsonify(analysis_data), 200
        
    except Exception as e:
        logger.error(f"Błąd podczas pobierania analizy: {str(e)}")
        return jsonify({"error": str(e)}), 500
