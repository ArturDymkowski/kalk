import os
import logging
from flask import Flask
from flask_cors import CORS
from config import config
from database.utils import init_db
from api.routes import api_bp

def create_app(config_name=None):
    """
    Tworzy i konfiguruje aplikację Flask.
    
    Args:
        config_name (str, optional): Nazwa konfiguracji do użycia
        
    Returns:
        Flask: Aplikacja Flask
    """
    # Jeśli nie podano nazwy konfiguracji, pobierz ją ze zmiennej środowiskowej
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    # Utwórz aplikację
    app = Flask(__name__)
    
    # Skonfiguruj CORS
    CORS(app)
    
    # Załaduj konfigurację
    app.config.from_object(config[config_name])
    
    # Skonfiguruj logowanie
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Inicjalizuj bazę danych
    init_db(app)
    
    # Zarejestruj blueprint API
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Dodaj podstawową trasę główną
    @app.route('/')
    def index():
        return {
            "status": "running",
            "version": "1.0.0",
            "app": "Vedic Astrology Calculator API"
        }
    
    return app

if __name__ == '__main__':
    # Utwórz aplikację
    app = create_app()
    
    # Uruchom serwer rozwojowy
    app.run(host='0.0.0.0', port=5000, debug=True)
