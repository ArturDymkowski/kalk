import unittest
import json
from datetime import datetime
from flask import url_for
from .. import create_app
from ..database.models import db, User, BirthChart, VargaChart, LifeArea, ChartAnalysis

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        """Konfiguruje aplikację testową przed każdym testem."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        # Inicjuj dane testowe
        self._create_test_data()
    
    def tearDown(self):
        """Czyści po testach."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def _create_test_data(self):
        """Tworzy dane testowe w bazie danych."""
        # Utwórz przykładowy obszar życia
        health_area = LifeArea(
            name="Zdrowie",
            description="Analiza zdrowia, chorób i karmy rodowej",
            prompt_template="Proszę o analizę zdrowia na podstawie kosmogramu: {{chart_data}}",
            varga_combination="D1,D6,D12"
        )
        db.session.add(health_area)
        
        # Utwórz przykładowy kosmogram
        test_chart = BirthChart(
            name="Jan Testowy",
            birth_date=datetime(1990, 1, 1, 12, 0, 0),
            latitude=52.2297,
            longitude=21.0122
        )
        db.session.add(test_chart)
        
        # Zapisz zmiany
        db.session.commit()
        
        # Zapisz ID do użycia w testach
        self.test_chart_id = test_chart.id
        self.test_area_id = health_area.id
    
    def test_health_check(self):
        """Testuje podstawową trasę do sprawdzenia zdrowia API."""
        response = self.client.get('/api/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
    
    def test_get_charts(self):
        """Testuje pobieranie listy kosmogramów."""
        response = self.client.get('/api/charts')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('charts', data)
        self.assertEqual(len(data['charts']), 1)
        self.assertEqual(data['charts'][0]['name'], "Jan Testowy")
    
    def test_get_chart_details(self):
        """Testuje pobieranie szczegółów kosmogramu."""
        response = self.client.get(f'/api/chart/{self.test_chart_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], self.test_chart_id)
        self.assertEqual(data['name'], "Jan Testowy")
        self.assertIn('latitude', data)
        self.assertIn('longitude', data)
    
    def test_get_life_areas(self):
        """Testuje pobieranie obszarów życia."""
        response = self.client.get('/api/life-areas')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('life_areas', data)
        self.assertEqual(len(data['life_areas']), 1)
        self.assertEqual(data['life_areas'][0]['name'], "Zdrowie")
    
    def test_create_chart(self):
        """Testuje tworzenie nowego kosmogramu."""
        # Dane do utworzenia kosmogramu
        chart_data = {
            "name": "Anna Testowa",
            "birth_date": "1995-05-15T14:30:00",
            "latitude": 54.3520,
            "longitude": 18.6466
        }
        
        response = self.client.post(
            '/api/chart',
            data=json.dumps(chart_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIn('chart_id', data)
        
        # Sprawdź, czy kosmogram został rzeczywiście dodany do bazy
        chart = BirthChart.query.filter_by(name="Anna Testowa").first()
        self.assertIsNotNone(chart)
    
    def test_update_life_area_prompt(self):
        """Testuje aktualizację promptu dla obszaru życia."""
        # Nowy szablon promptu
        new_prompt = "Nowy szablon promptu dla zdrowia: {{chart_data}}"
        
        response = self.client.put(
            f'/api/life-area/{self.test_area_id}',
            data=json.dumps({"prompt_template": new_prompt}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        
        # Sprawdź, czy prompt został faktycznie zaktualizowany
        area = LifeArea.query.get(self.test_area_id)
        self.assertEqual(area.prompt_template, new_prompt)
    
    def test_invalid_chart_request(self):
        """Testuje obsługę błędnych żądań przy tworzeniu kosmogramu."""
        # Niepełne dane - brak szerokości geograficznej
        invalid_data = {
            "name": "Test Niepełny",
            "birth_date": "2000-01-01T12:00:00",
            "longitude": 20.0
        }
        
        response = self.client.post(
            '/api/chart',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_nonexistent_chart(self):
        """Testuje odpowiedź na żądanie nieistniejącego kosmogramu."""
        response = self.client.get('/api/chart/9999')  # ID, które nie istnieje
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
