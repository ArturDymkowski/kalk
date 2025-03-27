import swisseph as swe
import math
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from .models import PlanetInfo, HouseInfo, AspectsInfo

# Stałe
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,  # Północny węzeł księżycowy (Rahu)
    'Ketu': -1,  # Południowy węzeł księżycowy (Ketu) - zostanie obliczony
    'Ascendant': -2  # Ascendent - zostanie obliczony 
}

SIGNS = [
    "Baran", "Byk", "Bliźnięta", "Rak", 
    "Lew", "Panna", "Waga", "Skorpion", 
    "Strzelec", "Koziorożec", "Wodnik", "Ryby"
]

HOUSE_SYSTEMS = {
    'Placidus': b'P',
    'Koch': b'K',
    'Regiomontanus': b'R',
    'Campanus': b'C',
    'Equal': b'E',
    'Whole Sign': b'W',
    'Sripati': b'I'  # System używany w astrologii wedyjskiej
}

# Mapowanie z numerów domów D1-D12 na ich nazwy
VARGA_NAMES = {
    1: "Rashi (D1)",
    2: "Hora (D2)",
    3: "Drekkana (D3)",
    4: "Chaturthamsa (D4)",
    5: "Panchamsa (D5)",
    6: "Shashthamsa (D6)",
    7: "Saptamsa (D7)",
    8: "Ashtamsa (D8)",
    9: "Navamsa (D9)",
    10: "Dasamsa (D10)",
    11: "Ekadasamsa (D11)",
    12: "Dvadasamsa (D12)"
}

class VedicAstroCalculator:
    """Kalkulator astrologii wedyjskiej."""
    
    def __init__(self, ephe_path=None):
        """
        Inicjalizuje kalkulator astrologii wedyjskiej.
        
        Args:
            ephe_path (str, optional): Ścieżka do plików efemerydy
        """
        if ephe_path:
            swe.set_ephe_path(ephe_path)
        else:
            # Użyj domyślnej ścieżki efemeryd
            swe.set_ephe_path()
        
        # Ustawienia dla astrologii wedyjskiej
        self.sidereal_mode = True
        self.ayanamsa = swe.SIDM_LAHIRI  # Popularny ayanamsa w astrologii wedyjskiej
        
        if self.sidereal_mode:
            swe.set_sid_mode(self.ayanamsa)
    
    def _normalize_longitude(self, longitude):
        """Normalizuje długość geograficzną do przedziału 0-360 stopni."""
        return longitude % 360
    
    def _get_sign(self, longitude):
        """Zwraca znak zodiaku na podstawie długości geograficznej."""
        sign_num = int(longitude / 30)
        return sign_num
    
    def _get_degrees_in_sign(self, longitude):
        """Zwraca pozycję w stopniach w obrębie znaku."""
        return longitude % 30
    
    def _get_local_timezone(self, latitude, longitude):
        """Określa strefę czasową na podstawie współrzędnych geograficznych."""
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=longitude, lat=latitude)
        return pytz.timezone(tz_name) if tz_name else pytz.UTC
    
    def _convert_to_utc(self, birth_datetime, latitude, longitude):
        """Konwertuje lokalny czas na UTC."""
        if birth_datetime.tzinfo is None:
            # Jeśli czas nie ma informacji o strefie czasowej, zakładamy lokalną strefę
            tz = self._get_local_timezone(latitude, longitude)
            local_dt = tz.localize(birth_datetime)
            return local_dt.astimezone(pytz.UTC)
        else:
            # Jeśli czas ma już strefę czasową, konwertujemy do UTC
            return birth_datetime.astimezone(pytz.UTC)
    
    def _calc_julian_day(self, dt):
        """Oblicza dzień juliański."""
        return swe.julday(dt.year, dt.month, dt.day, 
                          dt.hour + dt.minute/60.0 + dt.second/3600.0)
    
    def _calc_planet_position(self, jd, planet_id):
        """Oblicza pozycję planety."""
        if planet_id == -1:  # Ketu
            # Ketu jest zawsze 180 stopni od Rahu
            rahu_pos = swe.calc_ut(jd, swe.MEAN_NODE)[0]
            return (self._normalize_longitude(rahu_pos + 180), 0, 0)
        elif planet_id == -2:  # Ascendent
            raise ValueError("Ascendent musi być obliczony osobno.")
        else:
            return swe.calc_ut(jd, planet_id)[0:3]
    
    def _calc_ascendant(self, jd, latitude, longitude):
        """Oblicza ascendent (Lagna)."""
        # Uzyskaj domy w systemie Sripati
        houses, ascendant = swe.houses(jd, latitude, longitude, HOUSE_SYSTEMS['Sripati'])
        return ascendant
    
    def _calc_houses(self, jd, latitude, longitude):
        """Oblicza pozycje domów."""
        houses, ascendant = swe.houses(jd, latitude, longitude, HOUSE_SYSTEMS['Sripati'])
        return houses
    
    def _get_varga_longitude(self, longitude, varga_num):
        """
        Oblicza długość w określonej vardze.
        
        Args:
            longitude (float): Długość w D1 (Rasi)
            varga_num (int): Numer vargi (1-12)
            
        Returns:
            float: Długość w wybranej vardze
        """
        if varga_num == 1:
            # D1 (Rasi) - bez zmian
            return longitude
        elif varga_num == 2:
            # D2 (Hora)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            # Hora Słońca (znaki nieparzyste) i Hora Księżyca (znaki parzyste)
            if rasi % 2 == 0:  # Parzyste znaki
                if degree < 15:
                    return 30 * 4  # Księżyc - Rak
                else:
                    return 30 * 0  # Słońce - Baran
            else:  # Nieparzyste znaki
                if degree < 15:
                    return 30 * 0  # Słońce - Baran
                else:
                    return 30 * 4  # Księżyc - Rak
        elif varga_num == 3:
            # D3 (Drekkana)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            if degree < 10:
                return rasi * 30  # Pierwszy dekanat - ten sam znak
            elif degree < 20:
                return ((rasi + 4) % 12) * 30  # Drugi dekanat - znak + 4
            else:
                return ((rasi + 8) % 12) * 30  # Trzeci dekanat - znak + 8
        elif varga_num == 4:
            # D4 (Chaturthamsa)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            part = int(degree / 7.5)  # 30/4 = 7.5 stopni na część
            return ((rasi * 4 + part) % 12) * 30
        elif varga_num == 5:
            # D5 (Panchamsa)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            part = int(degree / 6)  # 30/5 = 6 stopni na część
            
            # Różny algorytm dla znaków ruchomych, stałych i zmiennych
            if rasi % 3 == 0:  # Ruchome znaki (Baran, Rak, Waga, Koziorożec)
                return ((rasi + part) % 12) * 30
            elif rasi % 3 == 1:  # Stałe znaki (Byk, Lew, Skorpion, Wodnik)
                return ((rasi + 4 + part) % 12) * 30
            else:  # Zmienne znaki (Bliźnięta, Panna, Strzelec, Ryby)
                return ((rasi + 8 + part) % 12) * 30
        elif varga_num == 6:
            # D6 (Shashthamsa)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            part = int(degree / 5)  # 30/6 = 5 stopni na część
            return ((rasi * 6 + part) % 12) * 30
        elif varga_num == 7:
            # D7 (Saptamsa)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            part = int(degree / (30/7))
            
            # Różny algorytm dla znaków nieparzystych i parzystych
            if rasi % 2 == 0:  # Parzyste znaki
                return ((rasi + 6 + part) % 12) * 30
            else:  # Nieparzyste znaki
                return ((rasi + part) % 12) * 30
        elif varga_num == 8:
            # D8 (Ashtamsa)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            part = int(degree / 3.75)  # 30/8 = 3.75 stopni na część
            return ((rasi * 8 + part) % 12) * 30
        elif varga_num == 9:
            # D9 (Navamsa) - klasyczna metoda
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            part = int(degree / 3.333333)  # 30/9 = 3.33 stopni na część
            
            # Dla znaków ognistych (Baran, Lew, Strzelec)
            if rasi % 4 == 0:
                return ((0 + part) % 12) * 30
            # Dla znaków ziemskich (Byk, Panna, Koziorożec)
            elif rasi % 4 == 1:
                return ((4 + part) % 12) * 30
            # Dla znaków powietrznych (Bliźnięta, Waga, Wodnik)
            elif rasi % 4 == 2:
                return ((8 + part) % 12) * 30
            # Dla znaków wodnych (Rak, Skorpion, Ryby)
            else:
                return ((0 + part) % 12) * 30
        elif varga_num == 10:
            # D10 (Dasamsa)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            part = int(degree / 3)  # 30/10 = 3 stopni na część
            
            # Różny algorytm dla znaków nieparzystych i parzystych
            if rasi % 2 == 0:  # Parzyste znaki
                return ((rasi * 10 + part) % 12) * 30
            else:  # Nieparzyste znaki
                return ((rasi * 10 + 9 + part) % 12) * 30
        elif varga_num == 11:
            # D11 (Ekadasamsa)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            part = int(degree / (30/11))
            return ((rasi * 11 + part) % 12) * 30
        elif varga_num == 12:
            # D12 (Dvadasamsa)
            rasi = self._get_sign(longitude)
            degree = self._get_degrees_in_sign(longitude)
            
            part = int(degree / 2.5)  # 30/12 = 2.5 stopni na część
            return ((rasi * 12 + part) % 12) * 30
        else:
            raise ValueError(f"Nieprawidłowy numer vargi: {varga_num}. Dopuszczalne wartości: 1-12.")
    
    def calculate_chart(self, birth_date, latitude, longitude, house_system='Sripati'):
        """
        Oblicza główny kosmogram (D1 Rasi).
        
        Args:
            birth_date (datetime): Data i godzina urodzenia
            latitude (float): Szerokość geograficzna miejsca urodzenia
            longitude (float): Długość geograficzna miejsca urodzenia
            house_system (str, optional): System domów
            
        Returns:
            dict: Dane kosmogramu
        """
        # Konwertuj do UTC i oblicz dzień juliański
        utc_dt = self._convert_to_utc(birth_date, latitude, longitude)
        jd = self._calc_julian_day(utc_dt)
        
        # Oblicz ascendent
        ascendant = self._calc_ascendant(jd, latitude, longitude)
        ascendant_sign = self._get_sign(ascendant)
        
        # Oblicz pozycje planet
        planets_data = {}
        for planet_name, planet_id in PLANETS.items():
            if planet_name == 'Ascendant':
                long, lat, dist = ascendant, 0, 0
            else:
                long, lat, dist = self._calc_planet_position(jd, planet_id)
            
            sign = self._get_sign(long)
            deg_in_sign = self._get_degrees_in_sign(long)
            
            planets_data[planet_name] = {
                'longitude': long,
                'latitude': lat,
                'distance': dist,
                'sign': sign,
                'sign_name': SIGNS[sign],
                'degrees_in_sign': deg_in_sign
            }
        
        # Oblicz domy
        houses = self._calc_houses(jd, latitude, longitude)
        houses_data = {}
        for i in range(12):
            house_cusp = houses[i]
            sign = self._get_sign(house_cusp)
            deg_in_sign = self._get_degrees_in_sign(house_cusp)
            
            houses_data[i+1] = {
                'longitude': house_cusp,
                'sign': sign,
                'sign_name': SIGNS[sign],
                'degrees_in_sign': deg_in_sign
            }
        
        # Tworzenie planety Ketu (180 stopni od Rahu)
        rahu_long = planets_data['Rahu']['longitude']
        ketu_long = self._normalize_longitude(rahu_long + 180)
        ketu_sign = self._get_sign(ketu_long)
        ketu_deg_in_sign = self._get_degrees_in_sign(ketu_long)
        
        planets_data['Ketu'] = {
            'longitude': ketu_long,
            'latitude': 0,
            'distance': 0,
            'sign': ketu_sign,
            'sign_name': SIGNS[ketu_sign],
            'degrees_in_sign': ketu_deg_in_sign
        }
        
        # Oblicz aspekty między planetami
        aspects = self._calculate_aspects(planets_data)
        
        return {
            'birth_date': birth_date.isoformat(),
            'latitude': latitude,
            'longitude': longitude,
            'julian_day': jd,
            'ayanamsa': swe.get_ayanamsa_ut(jd),
            'ascendant': {
                'longitude': ascendant,
                'sign': ascendant_sign,
                'sign_name': SIGNS[ascendant_sign],
                'degrees_in_sign': self._get_degrees_in_sign(ascendant)
            },
            'planets': planets_data,
            'houses': houses_data,
            'aspects': aspects
        }
    
    def calculate_varga(self, main_chart, varga_num):
        """
        Oblicza kosmogram vargi na podstawie głównego kosmogramu.
        
        Args:
            main_chart (dict): Główny kosmogram (D1 Rasi)
            varga_num (int): Numer vargi (1-12)
            
        Returns:
            dict: Dane kosmogramu vargi
        """
        if varga_num < 1 or varga_num > 12:
            raise ValueError(f"Nieprawidłowy numer vargi: {varga_num}. Dopuszczalne wartości: 1-12.")
        
        varga_chart = {
            'varga_type': f"D{varga_num}",
            'varga_name': VARGA_NAMES.get(varga_num, f"D{varga_num}"),
            'birth_date': main_chart['birth_date'],
            'latitude': main_chart['latitude'],
            'longitude': main_chart['longitude'],
            'julian_day': main_chart['julian_day'],
            'ayanamsa': main_chart['ayanamsa'],
            'planets': {},
        }
        
        # Konwertuj pozycje planet z D1 na wybraną vargę
        for planet_name, planet_data in main_chart['planets'].items():
            d1_longitude = planet_data['longitude']
            varga_longitude = self._get_varga_longitude(d1_longitude, varga_num)
            varga_sign = self._get_sign(varga_longitude)
            varga_deg_in_sign = self._get_degrees_in_sign(varga_longitude)
            
            varga_chart['planets'][planet_name] = {
                'longitude': varga_longitude,
                'sign': varga_sign,
                'sign_name': SIGNS[varga_sign],
                'degrees_in_sign': varga_deg_in_sign,
                'original_longitude': d1_longitude
            }
        
        # Oblicz aspekty dla vargi
        varga_chart['aspects'] = self._calculate_aspects(varga_chart['planets'])
        
        return varga_chart
    
    def calculate_all_vargas(self, birth_date, latitude, longitude):
        """
        Oblicza wszystkie vargi od D1 do D12.
        
        Args:
            birth_date (datetime): Data i godzina urodzenia
            latitude (float): Szerokość geograficzna miejsca urodzenia
            longitude (float): Długość geograficzna miejsca urodzenia
            
        Returns:
            dict: Słownik zawierający wszystkie vargi
        """
        # Najpierw oblicz główny kosmogram (D1 Rasi)
        main_chart = self.calculate_chart(birth_date, latitude, longitude)
        
        # Słownik na wszystkie vargi
        vargas = {'D1': main_chart}
        
        # Oblicz pozostałe vargi (D2-D12)
        for varga_num in range(2, 13):
            varga_chart = self.calculate_varga(main_chart, varga_num)
            vargas[f'D{varga_num}'] = varga_chart
        
        return vargas
    
    def _calculate_aspects(self, planets_data):
        """
        Oblicza aspekty między planetami według zasad astrologii wedyjskiej.
        
        Args:
            planets_data (dict): Dane planet
            
        Returns:
            list: Lista aspektów
        """
        aspects = []
        
        # Listę planet do obliczeń aspektów
        planet_names = list(planets_data.keys())
        
        # Definicje aspektów wedyjskich dla różnych planet (uproszczone)
        # W astrologii wedyjskiej każda planeta ma aspekty na określone domy od swojej pozycji
        vedic_aspects = {
            'Sun': [7],  # Aspekt na 7. dom
            'Moon': [7],
            'Mercury': [7],
            'Venus': [7],
            'Mars': [4, 7, 8],  # Aspekty na domy 4, 7 i 8
            'Jupiter': [5, 7, 9],  # Aspekty na domy 5, 7 i 9
            'Saturn': [3, 7, 10],  # Aspekty na domy 3, 7 i 10
            'Rahu': [5, 7, 9],  # Podobnie jak Jowisz
            'Ketu': [5, 7, 9],  # Podobnie jak Jowisz
            'Ascendant': []  # Ascendent nie rzuca aspektów w astrologii wedyjskiej
        }
        
        for i, p1_name in enumerate(planet_names):
            p1_data = planets_data[p1_name]
            p1_sign = p1_data['sign']
            
            # Oblicz aspekty dla tej planety
            for aspect_house in vedic_aspects.get(p1_name, []):
                # Oblicz znak, na który pada aspekt
                aspected_sign = (p1_sign + aspect_house - 1) % 12
                
                # Sprawdź, które planety są w tym znaku
                for p2_name in planet_names:
                    if p2_name != p1_name:  # Nie sprawdzaj aspektów planety na samą siebie
                        p2_data = planets_data[p2_name]
                        if p2_data['sign'] == aspected_sign:
                            aspects.append({
                                'planet1': p1_name,
                                'planet2': p2_name,
                                'aspect_type': f"Aspekt z domu {aspect_house}",
                                'strength': 100  # W astrologii wedyjskiej aspekty są pełne lub ich nie ma
                            })
        
        return aspects
