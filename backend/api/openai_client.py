import openai
import logging
import json
from flask import current_app

logger = logging.getLogger(__name__)

class OpenAIClient:
    """Klient API OpenAI do analizy kosmogramów wedyjskich."""
    
    def __init__(self, api_key=None):
        """
        Inicjalizuje klienta API OpenAI.
        
        Args:
            api_key (str, optional): Klucz API OpenAI. Jeśli nie podano, zostanie pobrany z konfiguracji.
        """
        self.api_key = api_key
        self.model = "gpt-4"  # Domyślny model
        
    def configure(self, api_key=None, model=None):
        """
        Konfiguruje klienta API.
        
        Args:
            api_key (str, optional): Klucz API OpenAI
            model (str, optional): Model do użycia
        """
        if api_key:
            self.api_key = api_key
            
        if model:
            self.model = model
        
        # Ustaw klucz API
        openai.api_key = self.api_key
        
    def analyze_chart(self, chart_data, prompt_template, max_tokens=2000):
        """
        Analizuje kosmogram wedyjski za pomocą API OpenAI.
        
        Args:
            chart_data (str): Sformatowane dane kosmogramu
            prompt_template (str): Szablon promptu do analizy
            max_tokens (int, optional): Maksymalna liczba tokenów w odpowiedzi
            
        Returns:
            str: Wynik analizy lub None w przypadku błędu
        """
        if not self.api_key:
            # Pobierz klucz API z konfiguracji aplikacji
            try:
                self.api_key = current_app.config['OPENAI_API_KEY']
                self.model = current_app.config.get('OPENAI_MODEL', self.model)
                openai.api_key = self.api_key
            except (RuntimeError, KeyError) as e:
                logger.error(f"Błąd konfiguracji OpenAI: {str(e)}")
                return None
        
        # Przygotuj prompt
        prompt = prompt_template.replace("{{chart_data}}", chart_data)
        
        try:
            # Wykonaj zapytanie do API OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Jesteś astrologiem wedyjskim z wieloletnim doświadczeniem. Twoja analiza jest dokładna, wnikliwa i oparta na klasycznych zasadach astrologii wedyjskiej."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Zwróć wynik analizy
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Błąd podczas analizy kosmogramu: {str(e)}")
            return None
            
    def analyze_area(self, chart_data, life_area, max_tokens=2000):
        """
        Analizuje określony obszar życia na podstawie kosmogramu.
        
        Args:
            chart_data (dict): Dane kosmogramu
            life_area (dict): Informacje o obszarze życia
            max_tokens (int, optional): Maksymalna liczba tokenów w odpowiedzi
            
        Returns:
            str: Wynik analizy lub None w przypadku błędu
        """
        from ..astro.utils import format_chart_for_ai
        
        # Przygotuj dane kosmogramu w formacie dla AI
        formatted_chart = format_chart_for_ai(chart_data, life_area)
        
        # Pobierz szablon promptu z obszaru życia
        prompt_template = life_area['prompt_template']
        
        # Wykonaj analizę
        return self.analyze_chart(formatted_chart, prompt_template, max_tokens)
