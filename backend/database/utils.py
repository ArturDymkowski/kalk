from .models import db, LifeArea, init_life_areas, BirthChart, VargaChart, ChartAnalysis
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def init_db(app):
    """Inicjalizuje bazę danych i tworzy wszystkie tabele."""
    with app.app_context():
        db.init_app(app)
        db.create_all()
        init_life_areas()
        logger.info("Baza danych zainicjalizowana pomyślnie.")

def save_birth_chart(name, birth_date, latitude, longitude, user_id=None):
    """
    Zapisuje nowy kosmogram urodzeniowy do bazy danych.
    
    Args:
        name (str): Imię i nazwisko osoby
        birth_date (datetime): Data i godzina urodzenia
        latitude (float): Szerokość geograficzna
        longitude (float): Długość geograficzna
        user_id (int, optional): ID użytkownika, jeśli dostępne
        
    Returns:
        BirthChart: Zapisany obiekt kosmogramu lub None w przypadku błędu
    """
    try:
        birth_chart = BirthChart(
            name=name,
            birth_date=birth_date,
            latitude=latitude,
            longitude=longitude,
            user_id=user_id
        )
        
        db.session.add(birth_chart)
        db.session.commit()
        return birth_chart
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Błąd podczas zapisywania kosmogramu: {str(e)}")
        return None

def save_varga_chart(birth_chart_id, varga_type, chart_data):
    """
    Zapisuje kosmogram vargi do bazy danych.
    
    Args:
        birth_chart_id (int): ID powiązanego kosmogramu urodzeniowego
        varga_type (str): Typ vargi (D1, D2, D3, itp.)
        chart_data (dict): Dane kosmogramu jako słownik
        
    Returns:
        VargaChart: Zapisany obiekt vargi lub None w przypadku błędu
    """
    try:
        varga_chart = VargaChart(
            birth_chart_id=birth_chart_id,
            varga_type=varga_type,
            data=chart_data  # Używamy settera właściwości data
        )
        
        db.session.add(varga_chart)
        db.session.commit()
        return varga_chart
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Błąd podczas zapisywania vargi {varga_type}: {str(e)}")
        return None

def save_chart_analysis(birth_chart_id, life_area_id, analysis_result):
    """
    Zapisuje analizę kosmogramu do bazy danych.
    
    Args:
        birth_chart_id (int): ID kosmogramu urodzeniowego
        life_area_id (int): ID analizowanego obszaru życia
        analysis_result (str): Wynik analizy
        
    Returns:
        ChartAnalysis: Zapisany obiekt analizy lub None w przypadku błędu
    """
    try:
        # Sprawdź, czy analiza już istnieje
        existing_analysis = ChartAnalysis.query.filter_by(
            birth_chart_id=birth_chart_id,
            life_area_id=life_area_id
        ).first()
        
        if existing_analysis:
            # Aktualizuj istniejącą analizę
            existing_analysis.analysis_result = analysis_result
            db.session.commit()
            return existing_analysis
        else:
            # Utwórz nową analizę
            analysis = ChartAnalysis(
                birth_chart_id=birth_chart_id,
                life_area_id=life_area_id,
                analysis_result=analysis_result
            )
            
            db.session.add(analysis)
            db.session.commit()
            return analysis
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Błąd podczas zapisywania analizy: {str(e)}")
        return None

def get_birth_charts():
    """
    Pobiera wszystkie kosmogramy urodzeniowe z bazy danych.
    
    Returns:
        list: Lista obiektów BirthChart
    """
    return BirthChart.query.order_by(BirthChart.created_at.desc()).all()

def get_birth_chart(chart_id):
    """
    Pobiera pojedynczy kosmogram urodzeniowy.
    
    Args:
        chart_id (int): ID kosmogramu
        
    Returns:
        BirthChart: Obiekt kosmogramu lub None, jeśli nie znaleziono
    """
    return BirthChart.query.get(chart_id)

def get_varga_charts(birth_chart_id):
    """
    Pobiera wszystkie kosmogramy varg dla określonego kosmogramu urodzeniowego.
    
    Args:
        birth_chart_id (int): ID kosmogramu urodzeniowego
        
    Returns:
        dict: Słownik varg, gdzie kluczem jest typ vargi (D1, D2, itd.)
    """
    vargas = VargaChart.query.filter_by(birth_chart_id=birth_chart_id).all()
    return {varga.varga_type: varga for varga in vargas}

def get_varga_chart(birth_chart_id, varga_type):
    """
    Pobiera określony kosmogram vargi.
    
    Args:
        birth_chart_id (int): ID kosmogramu urodzeniowego
        varga_type (str): Typ vargi (D1, D2, D3, itp.)
        
    Returns:
        VargaChart: Obiekt vargi lub None, jeśli nie znaleziono
    """
    return VargaChart.query.filter_by(
        birth_chart_id=birth_chart_id,
        varga_type=varga_type
    ).first()

def get_life_areas():
    """
    Pobiera wszystkie obszary życia.
    
    Returns:
        list: Lista obiektów LifeArea
    """
    return LifeArea.query.all()

def get_life_area(area_id):
    """
    Pobiera określony obszar życia.
    
    Args:
        area_id (int): ID obszaru życia
        
    Returns:
        LifeArea: Obiekt obszaru życia lub None, jeśli nie znaleziono
    """
    return LifeArea.query.get(area_id)

def get_chart_analyses(birth_chart_id=None, life_area_id=None):
    """
    Pobiera analizy kosmogramów.
    
    Args:
        birth_chart_id (int, optional): ID kosmogramu urodzeniowego
        life_area_id (int, optional): ID obszaru życia
        
    Returns:
        list: Lista obiektów ChartAnalysis
    """
    query = ChartAnalysis.query
    
    if birth_chart_id:
        query = query.filter_by(birth_chart_id=birth_chart_id)
        
    if life_area_id:
        query = query.filter_by(life_area_id=life_area_id)
        
    return query.order_by(ChartAnalysis.created_at.desc()).all()

def get_chart_analysis(analysis_id):
    """
    Pobiera pojedynczą analizę kosmogramu.
    
    Args:
        analysis_id (int): ID analizy
        
    Returns:
        ChartAnalysis: Obiekt analizy lub None, jeśli nie znaleziono
    """
    return ChartAnalysis.query.get(analysis_id)

def update_life_area_prompt(area_id, prompt_template):
    """
    Aktualizuje szablon promptu dla obszaru życia.
    
    Args:
        area_id (int): ID obszaru życia
        prompt_template (str): Nowy szablon promptu
        
    Returns:
        bool: True, jeśli aktualizacja się powiodła, False w przeciwnym razie
    """
    try:
        area = get_life_area(area_id)
        if area:
            area.prompt_template = prompt_template
            db.session.commit()
            return True
        return False
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Błąd podczas aktualizacji promptu: {str(e)}")
        return False
