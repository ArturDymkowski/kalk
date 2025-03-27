# Kalkulator Astrologii Wedyjskiej

Kompleksowa aplikacja do tworzenia kosmogramów wedyjskich i ich analizy przy użyciu sztucznej inteligencji. Aplikacja oblicza kosmogramy D1-D12 według klasycznych zasad astrologii wedyjskiej i umożliwia szczegółową analizę różnych obszarów życia.

## Struktura projektu

Projekt składa się z dwóch głównych części:

1. **Backend** - API napisane w Pythonie z frameworkiem Flask
2. **Frontend** - Interfejs użytkownika napisany w React.js

## Wymagania systemowe

- Python 3.8+
- Node.js 14+
- MySQL 5.7+
- Klucz API OpenAI

## Instalacja i konfiguracja

### Backend

1. Przejdź do katalogu backend:

```bash
cd backend
```

2. Stwórz i aktywuj wirtualne środowisko:

```bash
python -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate
```

3. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

4. Skonfiguruj bazę danych MySQL:

```sql
CREATE DATABASE vedic_astro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'vedic_user'@'localhost' IDENTIFIED BY 'haslo';
GRANT ALL PRIVILEGES ON vedic_astro.* TO 'vedic_user'@'localhost';
FLUSH PRIVILEGES;
```

5. Utwórz plik `.env` z konfiguracją:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=twoj_tajny_klucz_zmien_w_produkcji
DATABASE_URL=mysql+pymysql://vedic_user:haslo@localhost/vedic_astro
OPENAI_API_KEY=twoj_klucz_api_openai
OPENAI_MODEL=gpt-4
```

6. Zainicjalizuj bazę danych:

```bash
flask db init
flask db migrate
flask db upgrade
```

7. Uruchom serwer:

```bash
flask run
```

Backend będzie dostępny pod adresem http://localhost:5000

### Frontend

1. Przejdź do katalogu frontend:

```bash
cd frontend
```

2. Zainstaluj zależności:

```bash
npm install
```

3. Utwórz plik `.env` z konfiguracją:

```
REACT_APP_API_URL=http://localhost:5000/api
```

4. Uruchom aplikację:

```bash
npm start
```

Frontend będzie dostępny pod adresem http://localhost:3000

## Struktura bazy danych

Aplikacja używa następujących tabel:

- `users` - Dane użytkowników (opcjonalnie)
- `birth_charts` - Kosmogramy urodzeniowe
- `varga_charts` - Kosmogramy varg (D1-D12)
- `life_areas` - Obszary życia do analizy
- `chart_analyses` - Wyniki analiz kosmogramów

## Funkcje

1. **Obliczanie kosmogramów**
   - Tworzenie kosmogramu D1 (Rashi) na podstawie daty, godziny i miejsca urodzenia
   - Automatyczne obliczanie wszystkich varg od D1 do D12
   - Wykorzystanie precyzyjnych efemeryd astronomicznych

2. **Wizualizacja kosmogramów**
   - Interaktywna wizualizacja kosmogramów w stylu południowoindyjskim
   - Szczegółowe dane o pozycjach planet

3. **Analiza z wykorzystaniem AI**
   - Analiza zdrowia, finansów, związków, kariery i talentów
   - Wykorzystanie API OpenAI do interpretacji kosmogramów
   - Możliwość dostosowania promptów dla każdego obszaru życia

## Autor

Stworzone przez [Twoje imię/nazwa]
