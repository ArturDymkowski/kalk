import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

class Config:
    """Bazowa konfiguracja aplikacji."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')
    
    # Konfiguracja bazy danych
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://user:password@localhost/vedic_astro')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Konfiguracja OpenAI
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4')
    
    # Konfiguracja Swiss Ephemeris
    EPHE_PATH = os.environ.get('EPHE_PATH', os.path.join(os.path.dirname(__file__), 'astro', 'ephe'))


class DevelopmentConfig(Config):
    """Konfiguracja dla środowiska deweloperskiego."""
    DEBUG = True


class TestingConfig(Config):
    """Konfiguracja dla środowiska testowego."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test_user:test_password@localhost/test_vedic_astro'


class ProductionConfig(Config):
    """Konfiguracja dla środowiska produkcyjnego."""
    # Używaj bezpiecznego klucza w produkcji
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # W środowisku produkcyjnym używaj zmiennych środowiskowych
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


# Słownik konfiguracji do łatwego wyboru środowiska
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
