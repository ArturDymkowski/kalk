from datetime import datetime, timezone
import pytz
from timezonefinder import TimezoneFinder
import math

# Stałe
ZODIAC_SIGNS = [
    "Baran", "Byk", "Bliźnięta", "Rak", 
    "Lew", "Panna", "Waga", "Skorpion", 
    "Strzelec", "Koziorożec", "Wodnik", "Ryby"
]

ZODIAC_ELEMENTS = {
    "Baran": "Ogień", "Lew": "Ogień", "Strzelec": "Ogień",
    "Byk": "Ziemia", "Panna": "Ziemia", "Koziorożec": "Ziemia",
    "Bliźnięta": "Powietrze", "Waga": "Powietrze", "Wodnik": "Powietrze",
    "Rak": "Woda", "Skorpion": "Woda", "Ryby": "Woda"
}

ZODIAC_QUALITIES = {
    "Baran": "Kardynalny", "Rak": "Kardynalny", "Waga": "Kardynalny", "Koziorożec": "Kardynalny",
    "Byk": "Stały", "Lew": "Stały", "Skorpion": "Stały", "Wodnik": "Stały",
    "Bliźnięta": "Zmienny", "Panna": "Zmienny", "Strzelec": "Zmienny", "Ryby": "Zmienny"
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", 
    "Saturn", "Mercury", "Ketu", "Venus", "Sun", "Moon", 
    "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", 
    "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", 
    "Saturn", "Mercury"
]

PLANET_LORDS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
}

def get_local_timezone(latitude, longitude):
    """
    Określa strefę czasową na podstawie współrzędnych geograficznych.
    
    Args:
        latitude (float): Szerokość geograficzna
        longitude (float): Długość geograficzna
        
    Returns:
        tzinfo: Obiekt strefy czasowej
    """
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=longitude, lat=latitude)
    
    if tz_name:
        return pytz.timezone(tz_name)
    else:
        # Jeśli nie można określić strefy czasowej, użyj UTC
        return pytz.UTC


def normalize_degrees(degrees):
    """
    Normalizuje kąt do zakresu 0-360 stopni.
    
    Args:
        degrees (float): Kąt w stopniach
        
    Returns:
        float: Znormalizowany kąt
    """
    return degrees % 360


def degrees_to_dms(degrees):
    """
    Konwertuje stopnie dziesiętne na stopnie, minuty i sekundy.
    
    Args:
        degrees (float): Stopnie dziesiętne
        
    Returns:
        tuple: (stopnie, minuty, sekundy, kierunek)
    """
    # Normalizuj do 0-360
    degrees = normalize_degrees(degrees)
    
    # Oblicz całkowite stopnie
    d = int(degrees)
    
    # Oblicz minuty
    minutes_decimal = (degrees - d) * 60
    m = int(minutes_decimal)
    
    # Oblicz sekundy
    seconds_decimal = (minutes_decimal - m) * 60
    s = round(seconds_decimal)
    
    # Korekta, gdy sekundy wynoszą 60
    if s == 60:
        s = 0
        m += 1
    
    # Korekta, gdy minuty wynoszą 60
    if m == 60:
        m = 0
        d += 1
    
    # Uważaj na przypadek, gdy d = 360
    if d == 360:
        d = 0
    
    return (d, m, s)


def dms_to_string(dms):
    """
    Konwertuje stopnie, minuty i sekundy na czytelny string.
    
    Args:
        dms (tuple): (stopnie, minuty, sekundy)
        
    Returns:
        str: Sformatowana reprezentacja
    """
    d, m, s = dms
    return f"{d}° {m}' {s}\""


def degrees_to_sign_position(degrees):
    """
    Konwertuje pozycję w stopniach na znak zodiaku i pozycję w znaku.
    
    Args:
        degrees (float): Pozycja w stopniach (0-360)
        
    Returns:
        dict: Informacje o pozycji w znaku
    """
    # Normalizuj stopnie do zakresu 0-360
    degrees = normalize_degrees(degrees)
    
    # Oblicz znak zodiaku (0-11)
    sign_num = int(degrees / 30)
    
    # Oblicz pozycję w znaku (0-29.99...)
    position_in_sign = degrees % 30
    
    # Konwertuj pozycję w znaku na stopnie, minuty, sekundy
    dms = degrees_to_dms(position_in_sign)
    
    return {
        'sign_num': sign_num,
        'sign_name': ZODIAC_SIGNS[sign_num],
        'position_in_sign': position_in_sign,
        'position_dms': dms,
        'position_str': dms_to_string(dms)
    }


def get_nakshatra(longitude):
    """
    Określa nakshatrę (gwiazdozbiór księżycowy) na podstawie długości ekliptycznej.
    
    Args:
        longitude (float): Długość ekliptyczna (0-360)
        
    Returns:
        dict: Informacje o nakshatrze
    """
    # Każda nakshatra zajmuje 13°20' (13.3333... stopni)
    nakshatra_span = 360 / 27
    
    # Oblicz numer nakshatra (0-26)
    nakshatra_num = int(longitude / nakshatra_span)
    
    # Oblicz pozycję w nakshatrze
    position_in_nakshatra = longitude % nakshatra_span
    
    # Oblicz, jaki procent nakshatra został zakończony
    nakshatra_completion = position_in_nakshatra / nakshatra_span
    
    # Oblicz padę (ćwiartkę) nakshatra (1-4)
    pada = int(nakshatra_completion * 4) + 1
    
    return {
        'nakshatra_num': nakshatra_num,
        'nakshatra_name': NAKSHATRAS[nakshatra_num],
        'nakshatra_lord': NAKSHATRA_LORDS[nakshatra_num],
        'position_in_nakshatra': position_in_nakshatra,
        'nakshatra_completion': nakshatra_completion,
        'pada': pada
    }


def format_chart_for_ai(chart_data, life_area=None):
    """
    Formatuje dane kosmogramu do analizy przez AI.
    
    Args:
        chart_data (dict): Dane kosmogramu
        life_area (dict, optional): Informacje o obszarze życia
        
    Returns:
        str: Sformatowane dane kosmogramu
    """
    output = []
    
    # Dodaj informacje podstawowe
    output.append("== DANE KOSMOGRAMU WEDYJSKIEGO ==")
    output.append(f"Data urodzenia: {chart_data['birth_date']}")
    output.append(f"Lokalizacja: Szerokość {chart_data['latitude']}, Długość {chart_data['longitude']}")
    output.append(f"Ayanamsa: {chart_data['ayanamsa']:.2f}°")
    output.append("")
    
    # Dodaj informacje o ascendencie
    asc = chart_data['ascendant']
    output.append(f"Ascendent (Lagna): {ZODIAC_SIGNS[asc['sign']]} {asc['degrees_in_sign']:.2f}°")
    output.append("")
    
    # Dodaj informacje o planetach
    output.append("== POZYCJE PLANET ==")
    for planet_name, planet_data in chart_data['planets'].items():
        sign_name = planet_data['sign_name']
        deg = planet_data['degrees_in_sign']
        output.append(f"{planet_name}: {sign_name} {deg:.2f}°")
    output.append("")
    
    # Jeśli dostępne, dodaj informacje o domach
    if 'houses' in chart_data:
        output.append("== DOMY ==")
        for house_num, house_data in chart_data['houses'].items():
            sign_name = house_data['sign_name']
            deg = house_data['degrees_in_sign']
            output.append(f"Dom {house_num}: {sign_name} {deg:.2f}°")
        output.append("")
    
    # Jeśli dostępne, dodaj informacje o aspektach
    if 'aspects' in chart_data and chart_data['aspects']:
        output.append("== GŁÓWNE ASPEKTY ==")
        for aspect in chart_data['aspects']:
            if 'strength' in aspect and aspect['strength'] > 90:  # Pokaż tylko silne aspekty
                output.append(f"{aspect['planet1']} - {aspect['planet2']}: {aspect['aspect_type']}")
        output.append("")
    
    # Jeśli to kosmogram vargi, dodaj specyficzne informacje
    if 'varga_type' in chart_data:
        output.append(f"== KOSMOGRAM {chart_data['varga_type']} - {chart_data['varga_name']} ==")
        output.append("Ten kosmogram reprezentuje specyficzną vargę (harmonikę) w astrologii wedyjskiej.")
        output.append("")
    
    # Jeśli określony obszar życia, dodaj właściwy kontekst
    if life_area:
        output.append(f"== OBSZAR ŻYCIA: {life_area['name']} ==")
        output.append(f"{life_area['description']}")
        output.append(f"Uwzględnione vargi: {life_area['varga_combination']}")
        output.append("")
    
    return "\n".join(output)


def get_planet_dignity(planet, sign):
    """
    Określa godność planety w danym znaku zodiaku.
    
    Args:
        planet (str): Nazwa planety
        sign (int): Numer znaku zodiaku (0-11)
        
    Returns:
        str: Status godności
    """
    sign_name = ZODIAC_SIGNS[sign]
    
    # Moolatrikona - podstawowy znak planety
    moolatrikona = {
        'Sun': "Lew",
        'Moon': "Rak",
        'Mercury': "Panna",
        'Venus': "Waga",
        'Mars': "Baran",
        'Jupiter': "Strzelec",
        'Saturn': "Wodnik",
        'Rahu': None,  # Rahu i Ketu nie mają moolatrikony
        'Ketu': None
    }
    
    # Egzaltacja - najwyższa moc planety
    exaltation = {
        'Sun': "Baran",
        'Moon': "Byk",
        'Mercury': "Panna",
        'Venus': "Ryby",
        'Mars': "Koziorożec",
        'Jupiter': "Rak",
        'Saturn': "Waga",
        'Rahu': "Byk",
        'Ketu': "Skorpion"
    }
    
    # Upadek - najniższa moc planety
    debilitation = {
        'Sun': "Waga",
        'Moon': "Skorpion",
        'Mercury': "Ryby",
        'Venus': "Panna",
        'Mars': "Rak",
        'Jupiter': "Koziorożec",
        'Saturn': "Baran",
        'Rahu': "Skorpion",
        'Ketu': "Byk"
    }
    
    # Przyjaciele i wrogowie każdej planety
    friends = {
        'Sun': ["Moon", "Mars", "Jupiter"],
        'Moon': ["Sun", "Mercury"],
        'Mercury': ["Sun", "Venus"],
        'Venus': ["Mercury", "Saturn"],
        'Mars': ["Sun", "Moon", "Jupiter"],
        'Jupiter': ["Sun", "Moon", "Mars"],
        'Saturn': ["Mercury", "Venus"],
        'Rahu': ["Venus", "Saturn"],
        'Ketu': ["Mars", "Sun"]
    }
    
    enemies = {
        'Sun': ["Saturn", "Venus"],
        'Moon': ["Rahu", "Ketu"],
        'Mercury': ["Moon"],
        'Venus': ["Sun", "Moon"],
        'Mars': ["Mercury"],
        'Jupiter': ["Mercury", "Venus"],
        'Saturn': ["Sun", "Moon", "Mars"],
        'Rahu': ["Sun", "Moon"],
        'Ketu': ["Venus", "Mercury"]
    }
    
    # Określ lordów każdego znaku
    sign_lords = {
        "Baran": "Mars",
        "Byk": "Venus",
        "Bliźnięta": "Mercury",
        "Rak": "Moon",
        "Lew": "Sun",
        "Panna": "Mercury",
        "Waga": "Venus",
        "Skorpion": "Mars",
        "Strzelec": "Jupiter",
        "Koziorożec": "Saturn",
        "Wodnik": "Saturn",
        "Ryby": "Jupiter"
    }
    
    # Określ godność
    if sign_name == moolatrikona.get(planet):
        return "Moolatrikona"
    elif sign_name == exaltation.get(planet):
        return "Egzaltacja"
    elif sign_name == debilitation.get(planet):
        return "Upadek"
    else:
        # Sprawdź, czy planeta jest w swoim znaku
        sign_lord = sign_lords.get(sign_name)
        if sign_lord == planet:
            return "Własny znak"
        # Sprawdź, czy planeta jest w znaku przyjaciela
        elif sign_lord in friends.get(planet, []):
            return "Znak przyjaciela"
        # Sprawdź, czy planeta jest w znaku wroga
        elif sign_lord in enemies.get(planet, []):
            return "Znak wroga"
        else:
            return "Neutralny"


def get_chart_strength(chart_data):
    """
    Oblicza siłę kosmogramu na podstawie pozycji planet.
    
    Args:
        chart_data (dict): Dane kosmogramu
        
    Returns:
        dict: Ocena siły kosmogramu
    """
    strengths = {}
    total_strength = 0
    max_strength = 0
    
    for planet_name, planet_data in chart_data['planets'].items():
        # Pomiń Rahu i Ketu w niektórych obliczeniach
        if planet_name in ['Rahu', 'Ketu']:
            continue
            
        sign = planet_data['sign']
        dignity = get_planet_dignity(planet_name, sign)
        
        # Przypisz wartość punktową dla każdej godności
        if dignity == "Egzaltacja":
            strength = 10
        elif dignity == "Moolatrikona":
            strength = 9
        elif dignity == "Własny znak":
            strength = 8
        elif dignity == "Znak przyjaciela":
            strength = 6
        elif dignity == "Neutralny":
            strength = 5
        elif dignity == "Znak wroga":
            strength = 2
        elif dignity == "Upadek":
            strength = 0
        else:
            strength = 5  # Domyślnie neutralny
        
        # Dodaj do całkowitej siły
        strengths[planet_name] = {
            'dignity': dignity,
            'strength': strength
        }
        
        total_strength += strength
        max_strength += 10  # Maksymalna możliwa siła dla każdej planety
    
    # Oblicz procentową siłę kosmogramu
    percent_strength = (total_strength / max_strength) * 100 if max_strength > 0 else 0
    
    return {
        'planet_strengths': strengths,
        'total_strength': total_strength,
        'max_strength': max_strength,
        'percent_strength': percent_strength
    }


def analyze_houses(chart_data):
    """
    Analizuje domy kosmogramu.
    
    Args:
        chart_data (dict): Dane kosmogramu
        
    Returns:
        dict: Analiza domów
    """
    houses_analysis = {}
    
    for house_num, house_data in chart_data['houses'].items():
        house_num = int(house_num)  # Upewnij się, że numer domu jest liczbą całkowitą
        sign = house_data['sign']
        sign_name = house_data['sign_name']
        
        # Znajdź planety w tym domu
        planets_in_house = []
        for planet_name, planet_data in chart_data['planets'].items():
            if planet_data['sign'] == sign:
                planets_in_house.append(planet_name)
        
        # Określ lorda domu
        house_lord = None
        if sign_name == "Baran" or sign_name == "Skorpion":
            house_lord = "Mars"
        elif sign_name == "Byk" or sign_name == "Waga":
            house_lord = "Venus"
        elif sign_name == "Bliźnięta" or sign_name == "Panna":
            house_lord = "Mercury"
        elif sign_name == "Rak":
            house_lord = "Moon"
        elif sign_name == "Lew":
            house_lord = "Sun"
        elif sign_name == "Strzelec" or sign_name == "Ryby":
            house_lord = "Jupiter"
        elif sign_name == "Koziorożec" or sign_name == "Wodnik":
            house_lord = "Saturn"
        
        # Znajdź, w którym domu znajduje się lord tego domu
        lord_house = None
        if house_lord:
            lord_data = chart_data['planets'].get(house_lord)
            if lord_data:
                lord_sign = lord_data['sign']
                for h_num, h_data in chart_data['houses'].items():
                    if h_data['sign'] == lord_sign:
                        lord_house = int(h_num)
                        break
        
        houses_analysis[house_num] = {
            'sign': sign,
            'sign_name': sign_name,
            'lord': house_lord,
            'lord_house': lord_house,
            'planets': planets_in_house
        }
    
    return houses_analysis


def combine_varga_charts(charts_dict, varga_types):
    """
    Łączy dane z kilku kosmogramów varg w jeden zbiorczy kosmogram do analizy.
    
    Args:
        charts_dict (dict): Słownik zawierający kosmogramy varg
        varga_types (list): Lista typów varg do połączenia (np. ['D1', 'D9'])
        
    Returns:
        dict: Połączony kosmogram
    """
    if not charts_dict or not varga_types:
        return None
    
    # Używamy pierwszego kosmogramu jako podstawy
    first_varga = varga_types[0]
    if first_varga not in charts_dict:
        return None
        
    combined_chart = charts_dict[first_varga].copy()
    
    # Dodaj informacje o łączonych vargach
    combined_chart['combined_vargas'] = varga_types
    
    # Dla każdej kolejnej vargi dodajemy jej dane do kombinowanego kosmogramu
    for varga_type in varga_types[1:]:
        if varga_type not in charts_dict:
            continue
            
        varga_chart = charts_dict[varga_type]
        
        # Połącz dane planet z różnych varg
        for planet_name, planet_data in varga_chart['planets'].items():
            if planet_name not in combined_chart['planets']:
                combined_chart['planets'][planet_name] = {}
                
            combined_chart['planets'][planet_name][varga_type] = {
                'sign': planet_data['sign'],
                'sign_name': planet_data['sign_name'],
                'degrees_in_sign': planet_data['degrees_in_sign']
            }
    
    return combined_chart
