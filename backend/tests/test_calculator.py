import unittest
from datetime import datetime
import pytz
from ..astro.calculator import VedicAstroCalculator

class TestVedicAstroCalculator(unittest.TestCase):
    
    def setUp(self):
        """Inicjalizuje obiekt kalkulatora przed każdym testem."""
        self.calculator = VedicAstroCalculator()
    
    def test_normalize_longitude(self):
        """Testuje funkcję normalizacji długości geograficznej."""
        # Test podstawowej normalizacji
        self.assertEqual(self.calculator._normalize_longitude(30), 30)
        
        # Test normalizacji wartości poza zakresem
        self.assertEqual(self.calculator._normalize_longitude(370), 10)
        self.assertEqual(self.calculator._normalize_longitude(-10), 350)
        self.assertEqual(self.calculator._normalize_longitude(720), 0)
    
    def test_get_sign(self):
        """Testuje funkcję określania znaku zodiaku."""
        # Test dla różnych wartości długości
        self.assertEqual(self.calculator._get_sign(0), 0)    # Baran
        self.assertEqual(self.calculator._get_sign(45), 1)   # Byk
        self.assertEqual(self.calculator._get_sign(89), 2)   # Bliźnięta
        self.assertEqual(self.calculator._get_sign(100), 3)  # Rak
        self.assertEqual(self.calculator._get_sign(360), 0)  # Baran (normalizacja 360 -> 0)
    
    def test_get_degrees_in_sign(self):
        """Testuje funkcję określania stopni w znaku zodiaku."""
        # Test dla różnych wartości długości
        self.assertEqual(self.calculator._get_degrees_in_sign(0), 0)
        self.assertEqual(self.calculator._get_degrees_in_sign(31), 1)
        self.assertEqual(self.calculator._get_degrees_in_sign(59), 29)
        self.assertEqual(self.calculator._get_degrees_in_sign(360), 0)
    
    def test_calculate_chart_basic(self):
        """Testuje podstawowe obliczanie kosmogramu."""
        # Przykładowa data urodzenia
        birth_date = datetime(1990, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
        
        # Przykładowa lokalizacja (Warszawa)
        latitude = 52.2297
        longitude = 21.0122
        
        # Oblicz kosmogram
        chart = self.calculator.calculate_chart(birth_date, latitude, longitude)
        
        # Sprawdź podstawowe informacje o kosmogramie
        self.assertIsNotNone(chart)
        self.assertIn('planets', chart)
        self.assertIn('houses', chart)
        self.assertIn('ascendant', chart)
        
        # Sprawdź, czy wszystkie planety są obecne
        expected_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu', 'Ascendant']
        for planet in expected_planets:
            self.assertIn(planet, chart['planets'])
            
        # Sprawdź, czy wszystkie domy są obecne
        for house_num in range(1, 13):
            self.assertIn(str(house_num), chart['houses'])
    
    def test_calculate_varga(self):
        """Testuje obliczanie kosmogramów varg."""
        # Najpierw oblicz podstawowy kosmogram
        birth_date = datetime(1990, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
        latitude = 52.2297
        longitude = 21.0122
        main_chart = self.calculator.calculate_chart(birth_date, latitude, longitude)
        
        # Testuj obliczanie różnych varg
        for varga_num in range(1, 13):
            varga_chart = self.calculator.calculate_varga(main_chart, varga_num)
            
            # Sprawdź podstawowe informacje o vardze
            self.assertIsNotNone(varga_chart)
            self.assertEqual(varga_chart['varga_type'], f"D{varga_num}")
            self.assertIn('planets', varga_chart)
            
            # Sprawdź, czy wszystkie planety są obecne
            for planet in main_chart['planets']:
                self.assertIn(planet, varga_chart['planets'])
    
    def test_get_varga_longitude_special_cases(self):
        """Testuje specyficzne przypadki obliczania długości varg."""
        # D9 (Navamsa) - klasyczny test
        # W D9 każdy znak jest podzielony na 9 części
        # Pierwszy pada Navamsy to 0°-3°20' w każdym znaku
        
        # Baran 0° (0°) -> Baran w D9 (0°)
        self.assertAlmostEqual(
            self.calculator._get_varga_longitude(0, 9) % 30,
            0,
            places=1
        )
        
        # Baran 5° (5°) -> Byk w D9 (5° padają w 2. padzie)
        self.assertAlmostEqual(
            self.calculator._get_varga_longitude(5, 9) / 30,
            4/12,  # Oczekiwany znak w D9 (Byk dla ogniowego znaku)
            places=1
        )
    
    def test_varga_d1_identity(self):
        """Sprawdza, czy D1 (Rasi) jest identyczna z wejściowym kosmogramem."""
        longitude = 45.5  # Byk 15°30'
        varga_d1 = self.calculator._get_varga_longitude(longitude, 1)
        
        # D1 nie zmienia położenia
        self.assertEqual(varga_d1, longitude)

if __name__ == '__main__':
    unittest.main()
