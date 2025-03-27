class PlanetInfo:
    """Klasa przechowująca informacje o planecie."""
    
    def __init__(self, name, longitude, latitude=0, distance=0, speed=0, retrograde=False):
        """
        Inicjalizuje informacje o planecie.
        
        Args:
            name (str): Nazwa planety
            longitude (float): Pozycja w długości ekliptycznej (0-360)
            latitude (float, optional): Szerokość ekliptyczna
            distance (float, optional): Odległość
            speed (float, optional): Prędkość
            retrograde (bool, optional): Czy planeta jest w ruchu wstecznym
        """
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.distance = distance
        self.speed = speed
        self.retrograde = retrograde
        
        # Oblicz znak i stopnie w znaku
        self.sign = int(longitude / 30)
        self.degrees_in_sign = longitude % 30
        self.minutes = (self.degrees_in_sign - int(self.degrees_in_sign)) * 60
        
    def to_dict(self):
        """Konwertuje informacje o planecie na słownik."""
        return {
            'name': self.name,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'distance': self.distance,
            'speed': self.speed,
            'retrograde': self.retrograde,
            'sign': self.sign,
            'degrees_in_sign': self.degrees_in_sign,
            'minutes': self.minutes
        }


class HouseInfo:
    """Klasa przechowująca informacje o domu astrologicznym."""
    
    def __init__(self, house_number, cusp_longitude, sign=None):
        """
        Inicjalizuje informacje o domu.
        
        Args:
            house_number (int): Numer domu (1-12)
            cusp_longitude (float): Długość ekliptyczna początku domu
            sign (int, optional): Znak zodiaku, w którym znajduje się cuspida
        """
        self.house_number = house_number
        self.cusp_longitude = cusp_longitude
        
        # Oblicz znak i stopnie
        if sign is None:
            self.sign = int(cusp_longitude / 30)
        else:
            self.sign = sign
            
        self.degrees_in_sign = cusp_longitude % 30
        
    def to_dict(self):
        """Konwertuje informacje o domu na słownik."""
        return {
            'house_number': self.house_number,
            'cusp_longitude': self.cusp_longitude,
            'sign': self.sign,
            'degrees_in_sign': self.degrees_in_sign
        }


class AspectsInfo:
    """Klasa do obliczania i przechowywania aspektów między planetami."""

    def __init__(self):
        """Inicjalizuje obiekt do obliczania aspektów."""
        # Definicje standardowych aspektów (kąt i orb)
        self.standard_aspects = {
            'Koniunkcja': {'angle': 0, 'orb': 10},
            'Opozycja': {'angle': 180, 'orb': 10},
            'Trygon': {'angle': 120, 'orb': 8},
            'Kwadratura': {'angle': 90, 'orb': 8},
            'Sekstyl': {'angle': 60, 'orb': 6}
        }
        
        # Wedyjskie aspekty specjalne dla każdej planety
        self.vedic_special_aspects = {
            'Mars': [4, 7, 8],         # Mars aspektuje domy 4, 7 i 8 od swojej pozycji
            'Jupiter': [5, 7, 9],      # Jowisz aspektuje domy 5, 7 i 9
            'Saturn': [3, 7, 10],      # Saturn aspektuje domy 3, 7 i 10
            'Rahu': [5, 7, 9],         # Rahu podobnie jak Jowisz
            'Ketu': [5, 7, 9]          # Ketu podobnie jak Jowisz
        }

    def calculate_angle(self, longitude1, longitude2):
        """
        Oblicza kąt między dwoma punktami na zodiaku.
        
        Args:
            longitude1 (float): Długość ekliptyczna pierwszego punktu
            longitude2 (float): Długość ekliptyczna drugiego punktu
            
        Returns:
            float: Kąt między punktami w zakresie 0-180 stopni
        """
        diff = abs(longitude1 - longitude2) % 360
        return min(diff, 360 - diff)

    def is_aspect(self, angle, aspect_type):
        """
        Sprawdza, czy dany kąt tworzy aspekt określonego typu.
        
        Args:
            angle (float): Kąt między planetami
            aspect_type (str): Typ aspektu
            
        Returns:
            bool: True, jeśli kąt tworzy aspekt, False w przeciwnym razie
        """
        if aspect_type not in self.standard_aspects:
            return False
            
        aspect_angle = self.standard_aspects[aspect_type]['angle']
        orb = self.standard_aspects[aspect_type]['orb']
        
        return abs(angle - aspect_angle) <= orb

    def calculate_aspects(self, planets):
        """
        Oblicza wszystkie aspekty między planetami.
        
        Args:
            planets (dict): Słownik z informacjami o planetach
            
        Returns:
            list: Lista aspektów
        """
        aspects = []
        planet_names = list(planets.keys())
        
        # Oblicz standardowe aspekty
        for i in range(len(planet_names)):
            for j in range(i + 1, len(planet_names)):
                planet1 = planet_names[i]
                planet2 = planet_names[j]
                
                longitude1 = planets[planet1]['longitude']
                longitude2 = planets[planet2]['longitude']
                
                angle = self.calculate_angle(longitude1, longitude2)
                
                for aspect_type, aspect_data in self.standard_aspects.items():
                    if self.is_aspect(angle, aspect_type):
                        # Oblicz siłę aspektu (im bliżej dokładnego kąta, tym silniejszy)
                        exact_angle = aspect_data['angle']
                        orb = aspect_data['orb']
                        diff = abs(angle - exact_angle)
                        strength = 100 - (diff / orb * 100)
                        
                        aspects.append({
                            'planet1': planet1,
                            'planet2': planet2,
                            'aspect_type': aspect_type,
                            'angle': angle,
                            'exact_angle': exact_angle,
                            'orb': diff,
                            'strength': strength
                        })
        
        # Oblicz wedyjskie aspekty specjalne
        for planet_name in planet_names:
            if planet_name in self.vedic_special_aspects:
                planet_sign = planets[planet_name]['sign']
                
                for house_offset in self.vedic_special_aspects[planet_name]:
                    # Oblicz znak zodiaku, na który rzucany jest aspekt
                    aspected_sign = (planet_sign + house_offset - 1) % 12
                    
                    # Sprawdź, które planety są w tym znaku
                    for target_planet in planet_names:
                        if target_planet != planet_name and planets[target_planet]['sign'] == aspected_sign:
                            aspects.append({
                                'planet1': planet_name,
                                'planet2': target_planet,
                                'aspect_type': f"Wedyjski aspekt z domu {house_offset}",
                                'strength': 100  # W astrologii wedyjskiej aspekty są pełne
                            })
        
        return aspects


class VedicChartDasa:
    """Klasa do obliczania okresów Dasha w astrologii wedyjskiej."""
    
    def __init__(self, birth_date, moon_longitude):
        """
        Inicjalizuje system Vimshottari Dasha.
        
        Args:
            birth_date (datetime): Data urodzenia
            moon_longitude (float): Długość ekliptyczna Księżyca
        """
        self.birth_date = birth_date
        self.moon_longitude = moon_longitude
        
        # Definicja okresów poszczególnych planet (w latach)
        self.dasha_periods = {
            'Ketu': 7,
            'Venus': 20,
            'Sun': 6,
            'Moon': 10,
            'Mars': 7,
            'Rahu': 18,
            'Jupiter': 16,
            'Saturn': 19,
            'Mercury': 17
        }
        
        # Porządek planet w systemie Vimshottari
        self.dasha_order = [
            'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 
            'Rahu', 'Jupiter', 'Saturn', 'Mercury'
        ]
        
        # Suma wszystkich okresów (120 lat)
        self.total_dasha_years = sum(self.dasha_periods.values())
        
        # Oblicz nakshatra (gwiazdozbiór księżycowy)
        self.nakshatra = self._calculate_nakshatra()
        
        # Oblicz pozostałą część bieżącej nakshatra w momencie urodzenia
        self.nakshatra_remainder = self._calculate_nakshatra_remainder()
        
        # Oblicz główną planetę (mahadasha) w momencie urodzenia
        self.birth_mahadasha = self._calculate_birth_mahadasha()
        
    def _calculate_nakshatra(self):
        """
        Oblicza nakshatra (gwiazdozbiór księżycowy) na podstawie pozycji Księżyca.
        
        Returns:
            int: Numer nakshatra (0-26)
        """
        # Każda nakshatra zajmuje 13°20' (13.33333... stopni)
        nakshatra_span = 360 / 27
        
        # Oblicz numer nakshatra (0-26)
        return int(self.moon_longitude / nakshatra_span)
    
    def _calculate_nakshatra_remainder(self):
        """
        Oblicza pozostałą część bieżącej nakshatra w momencie urodzenia.
        
        Returns:
            float: Pozostała część nakshatra (0-1)
        """
        nakshatra_span = 360 / 27
        nakshatra_start = self.nakshatra * nakshatra_span
        
        # Oblicz, jaką część nakshatra przeszedł Księżyc
        portion_elapsed = (self.moon_longitude - nakshatra_start) / nakshatra_span
        
        return portion_elapsed
    
    def _calculate_birth_mahadasha(self):
        """
        Oblicza główną planetę (mahadasha) w momencie urodzenia.
        
        Returns:
            dict: Informacje o mahadasha urodzeniowej
        """
        # Władcą nakshatra jest planeta w określonej kolejności
        # Każda planeta rządzi 3 nakshatrami
        nakshatra_lords = {}
        for i in range(27):
            nakshatra_lords[i] = self.dasha_order[i % 9]
        
        # Oblicz planetę rządzącą daną nakshatrą
        ruling_planet = nakshatra_lords[self.nakshatra]
        
        # Indeks planety w porządku dasha
        planet_index = self.dasha_order.index(ruling_planet)
        
        # Oblicz, ile z okresu dasha upłynęło
        dasha_years = self.dasha_periods[ruling_planet]
        years_elapsed = dasha_years * self.nakshatra_remainder
        
        return {
            'planet': ruling_planet,
            'period_years': dasha_years,
            'years_elapsed': years_elapsed,
            'years_remaining': dasha_years - years_elapsed
        }
    
    def calculate_dashas(self, years_ahead=120):
        """
        Oblicza sekwencję okresów Dasha od urodzenia.
        
        Args:
            years_ahead (int, optional): Ile lat do przodu obliczyć
            
        Returns:
            list: Lista okresów Dasha
        """
        dashas = []
        
        # Rozpocznij od mahadasha w momencie urodzenia
        current_planet = self.birth_mahadasha['planet']
        current_planet_index = self.dasha_order.index(current_planet)
        
        # Dodaj pozostałą część bieżącej mahadasha
        start_date = self.birth_date
        remaining_years = self.birth_mahadasha['years_remaining']
        
        if remaining_years > 0:
            end_date = self._add_years_to_date(start_date, remaining_years)
            
            dashas.append({
                'planet': current_planet,
                'level': 'Mahadasha',
                'start_date': start_date,
                'end_date': end_date,
                'years': remaining_years
            })
            
            start_date = end_date
        
        # Oblicz kolejne mahadashas
        years_calculated = remaining_years
        current_planet_index = (current_planet_index + 1) % 9
        
        while years_calculated < years_ahead:
            current_planet = self.dasha_order[current_planet_index]
            period_years = self.dasha_periods[current_planet]
            
            # Jeśli dodanie całego okresu przekroczyłoby limit, ogranicz
            if years_calculated + period_years > years_ahead:
                period_years = years_ahead - years_calculated
            
            end_date = self._add_years_to_date(start_date, period_years)
            
            dashas.append({
                'planet': current_planet,
                'level': 'Mahadasha',
                'start_date': start_date,
                'end_date': end_date,
                'years': period_years
            })
            
            start_date = end_date
            years_calculated += period_years
            current_planet_index = (current_planet_index + 1) % 9
        
        return dashas
    
    def _add_years_to_date(self, date, years):
        """
        Dodaje określoną liczbę lat do daty.
        
        Args:
            date (datetime): Data początkowa
            years (float): Liczba lat do dodania
            
        Returns:
            datetime: Nowa data
        """
        # Proste dodanie lat (ignoruje lata przestępne dla uproszczenia)
        # W rzeczywistej implementacji należałoby użyć dokładniejszego algorytmu
        import datetime
        
        # Rozdziel lata całkowite i część ułamkową
        whole_years = int(years)
        fractional_years = years - whole_years
        
        # Dodaj całkowite lata
        new_date = date.replace(year=date.year + whole_years)
        
        # Dodaj część ułamkową jako dni
        days_to_add = int(fractional_years * 365.25)
        new_date = new_date + datetime.timedelta(days=days_to_add)
        
        return new_date
