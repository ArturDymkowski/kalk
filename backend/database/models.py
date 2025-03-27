from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """Model użytkownika - opcjonalny, jeśli chcemy dodać system logowania."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacje
    charts = db.relationship('BirthChart', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'


class BirthChart(db.Model):
    """Model kosmogramu urodzeniowego."""
    __tablename__ = 'birth_charts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacje
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    vargas = db.relationship('VargaChart', backref='birth_chart', lazy=True)
    analyses = db.relationship('ChartAnalysis', backref='birth_chart', lazy=True)
    
    def __repr__(self):
        return f'<BirthChart {self.name} - {self.birth_date}>'


class VargaChart(db.Model):
    """Model kosmogramu vargi."""
    __tablename__ = 'varga_charts'
    
    id = db.Column(db.Integer, primary_key=True)
    birth_chart_id = db.Column(db.Integer, db.ForeignKey('birth_charts.id'), nullable=False)
    varga_type = db.Column(db.String(20), nullable=False)  # D1, D2, D3, etc.
    chart_data = db.Column(db.Text, nullable=False)  # JSON z danymi kosmogramu
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<VargaChart {self.varga_type} for Chart #{self.birth_chart_id}>'
    
    @property
    def data(self):
        """Deserializuj dane kosmogramu z JSON."""
        return json.loads(self.chart_data)
    
    @data.setter
    def data(self, value):
        """Serializuj dane kosmogramu do JSON."""
        self.chart_data = json.dumps(value)


class LifeArea(db.Model):
    """Model obszaru życia do analizy."""
    __tablename__ = 'life_areas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    prompt_template = db.Column(db.Text, nullable=False)
    varga_combination = db.Column(db.String(50), nullable=False)  # np. "D1,D6,D12" dla zdrowia
    
    # Relacje
    analyses = db.relationship('ChartAnalysis', backref='life_area', lazy=True)
    
    def __repr__(self):
        return f'<LifeArea {self.name}>'


class ChartAnalysis(db.Model):
    """Model analizy kosmogramu."""
    __tablename__ = 'chart_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    birth_chart_id = db.Column(db.Integer, db.ForeignKey('birth_charts.id'), nullable=False)
    life_area_id = db.Column(db.Integer, db.ForeignKey('life_areas.id'), nullable=False)
    analysis_result = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChartAnalysis for Chart #{self.birth_chart_id}, Area: {self.life_area_id}>'


# Inicjalizacja domyślnych obszarów życia
def init_life_areas():
    """Inicjalizuje domyślne obszary życia w bazie danych."""
    default_areas = [
        {
            'name': 'Zdrowie',
            'description': 'Analiza zdrowia, chorób i karmy rodowej',
            'prompt_template': '''Przeprowadź dokładną analizę zdrowia na podstawie kosmogramu wedyjskiego. 
Uwzględnij informacje z kosmogramu głównego (D1), kosmogramu chorób (D6) oraz karmy rodowej (D12).
Zwróć uwagę na:
1. Ogólną konstytucję fizyczną i wrodzone predyspozycje zdrowotne
2. Potencjalne słabe punkty organizmu i podatność na choroby
3. Dziedziczne tendencje zdrowotne
4. Zalecenia dotyczące profilaktyki i wzmacniania zdrowia

Dane kosmogramu:
{{chart_data}}''',
            'varga_combination': 'D1,D6,D12'
        },
        {
            'name': 'Finanse',
            'description': 'Analiza finansów, bogactwa i zysków',
            'prompt_template': '''Przeprowadź dokładną analizę sytuacji finansowej na podstawie kosmogramu wedyjskiego.
Uwzględnij informacje z kosmogramu głównego (D1), kosmogramu bogactwa (D2) oraz kosmogramu zysków (D11).
Zwróć uwagę na:
1. Naturalne tendencje do gromadzenia majątku
2. Najlepsze źródła dochodów i metody zarabiania
3. Potencjalne wyzwania finansowe i jak je przezwyciężyć
4. Strategie inwestycyjne pasujące do profilu astrologicznego
5. Okresy prosperity i możliwych trudności finansowych

Dane kosmogramu:
{{chart_data}}''',
            'varga_combination': 'D1,D2,D11'
        },
        {
            'name': 'Związki',
            'description': 'Analiza związków, małżeństwa i relacji z dziećmi',
            'prompt_template': '''Przeprowadź dokładną analizę relacji międzyludzkich na podstawie kosmogramu wedyjskiego.
Uwzględnij informacje z kosmogramu głównego (D1), kosmogramu małżeństwa (D9) oraz kosmogramu dzieci (D7).
Zwróć uwagę na:
1. Naturalne tendencje w relacjach i partnerstwo
2. Jakość i charakter potencjalnego małżeństwa
3. Kompatybilność z partnerem/partnerką
4. Relacje z dziećmi i potencjał rodzicielski
5. Wyzwania w relacjach i jak je przezwyciężyć

Dane kosmogramu:
{{chart_data}}''',
            'varga_combination': 'D1,D9,D7'
        },
        {
            'name': 'Kariera',
            'description': 'Analiza kariery, sukcesu zawodowego i przychodów',
            'prompt_template': '''Przeprowadź dokładną analizę kariery zawodowej na podstawie kosmogramu wedyjskiego.
Uwzględnij informacje z kosmogramu głównego (D1), kosmogramu kariery (D10) oraz kosmogramu przychodów (D11).
Zwróć uwagę na:
1. Naturalne talenty i predyspozycje zawodowe
2. Najlepsze ścieżki kariery i dziedziny działalności
3. Relacje z przełożonymi i współpracownikami
4. Potencjał do osiągnięcia sukcesu i pozycji społecznej
5. Okresy sprzyjające rozwojowi zawodowemu

Dane kosmogramu:
{{chart_data}}''',
            'varga_combination': 'D1,D10,D11'
        },
        {
            'name': 'Talenty',
            'description': 'Analiza talentów, kreatywności i rozwoju duchowego',
            'prompt_template': '''Przeprowadź dokładną analizę talentów i kreatywności na podstawie kosmogramu wedyjskiego.
Uwzględnij informacje z kosmogramu głównego (D1), kosmogramu kreatywności (D5) oraz kosmogramu rozwoju duchowego (D9).
Zwróć uwagę na:
1. Wrodzone talenty i zdolności
2. Potencjał twórczy i artystyczny
3. Ścieżka rozwoju osobistego i duchowego
4. Jak najlepiej wykorzystać swoje naturalne dary
5. Karmiczne wpływy z poprzednich wcieleń

Dane kosmogramu:
{{chart_data}}''',
            'varga_combination': 'D1,D5,D9'
        }
    ]
    
    for area_data in default_areas:
        area = LifeArea.query.filter_by(name=area_data['name']).first()
        if not area:
            area = LifeArea(**area_data)
            db.session.add(area)
    
    db.session.commit()
