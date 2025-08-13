# YouTube Statistics Web Application

Aplikacja web do wizualizacji statystyk YouTube z wykorzystaniem Flask, PostgreSQL i D3.js.

## Funkcjonalności

- **Strona główna** - Dashboard z ogólnymi statystykami
- **Playlisty** - Wykresy słupkowe dla każdej playlisty (wyświetlenia per film)
- **Top Playlisty** - Ranking najpopularniejszych playlist

## Wymagania

- Python 3.8+
- PostgreSQL
- Dane YouTube (z aplikacji data_loader)

## Instalacja

1. **Zainstaluj zależności:**
```bash
cd app/website
pip install -r requirements.txt
```

2. **Skonfiguruj zmienne środowiskowe:**
Skopiuj plik `.env` z folderu `app/data_loader/` lub utwórz nowy:
```bash
cp ../data_loader/.env .
```

3. **Upewnij się, że baza danych jest skonfigurowana:**
- PostgreSQL musi być uruchomiony
- Baza danych musi zawierać dane z `data_loader`
- Zmienne środowiskowe muszą być poprawnie ustawione

## Uruchomienie

### Opcja 1: Bezpośrednie uruchomienie
```bash
cd app/website
python run_website.py
```

### Opcja 2: Uruchomienie przez Flask
```bash
cd app/website
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

### Opcja 3: Uruchomienie z ustawieniami środowiskowymi
```bash
cd app/website
FLASK_HOST=0.0.0.0 FLASK_PORT=5000 FLASK_DEBUG=True python run_website.py
```

## Dostęp do aplikacji

Po uruchomieniu aplikacja będzie dostępna pod adresem:
- **Strona główna:** http://localhost:5000/
- **Playlisty:** http://localhost:5000/playlists/
- **Top Playlisty:** http://localhost:5000/top-playlists/

## Struktura projektu

```
app/website/
├── app.py                 # Główna aplikacja Flask
├── database.py            # Funkcje do obsługi bazy danych
├── requirements.txt       # Zależności Python
├── run_website.py         # Skrypt uruchamiający
├── README.md             # Ten plik
├── routes/               # Blueprinty Flask
│   ├── __init__.py
│   ├── main.py           # Strona główna
│   ├── playlists.py      # Wykresy playlist
│   └── top_playlists.py  # Ranking playlist
├── static/               # Pliki statyczne
│   ├── css/
│   │   └── style.css     # Style CSS
│   └── js/
│       └── main.js       # JavaScript
└── templates/            # Szablony HTML
    ├── base.html         # Podstawowy layout
    ├── index.html        # Strona główna
    ├── playlists.html    # Wykresy playlist
    └── top_playlists.html # Ranking playlist
```

## Technologie

- **Backend:** Flask (Python)
- **Baza danych:** PostgreSQL
- **Frontend:** Bootstrap 5, D3.js
- **Wykresy:** D3.js (interaktywne wykresy słupkowe)
- **Styling:** CSS3 z animacjami

## Funkcje wykresów

- **Interaktywne tooltips** - pokazują dokładne wartości przy najechaniu
- **Responsywny design** - działa na wszystkich urządzeniach
- **Animacje** - płynne przejścia i efekty hover
- **Sortowanie** - dane są sortowane według wyświetleń

## Rozwiązywanie problemów

### Błąd połączenia z bazą danych
1. Sprawdź czy PostgreSQL jest uruchomiony
2. Sprawdź zmienne środowiskowe w pliku `.env`
3. Upewnij się, że baza danych zawiera dane

### Błąd importu modułów
1. Upewnij się, że jesteś w folderze `app/website`
2. Sprawdź czy wszystkie zależności są zainstalowane
3. Sprawdź czy ścieżka do `data_loader` jest poprawna

### Błąd portu
1. Zmień port w zmiennej `FLASK_PORT`
2. Sprawdź czy port nie jest zajęty przez inną aplikację

## Rozwój

### Dodawanie nowych wykresów
1. Utwórz nowy blueprint w folderze `routes/`
2. Dodaj funkcję w `database.py` do pobierania danych
3. Utwórz szablon HTML w folderze `templates/`
4. Dodaj JavaScript dla wykresu D3.js

### Modyfikacja stylów
- Edytuj plik `static/css/style.css`
- Dodaj nowe klasy CSS według potrzeb

### Dodawanie nowych funkcji
- Dodaj nowe endpointy w odpowiednich blueprintach
- Rozszerz funkcje w `database.py`
- Zaktualizuj szablony HTML i JavaScript

## Licencja

Ten projekt jest częścią większego systemu do analizy statystyk YouTube. 