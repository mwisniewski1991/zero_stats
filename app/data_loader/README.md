# YouTube Data Loader

Aplikacja do pobierania i przechowywania danych o filmach YouTube z kanału.

## Funkcjonalności

- Pobieranie wszystkich playlist z kanału YouTube
- Pobieranie filmów z każdej playlisty wraz ze statystykami
- Zapisywanie danych do bazy PostgreSQL
- Ciągłe monitorowanie nowych filmów
- Aktualizacja statystyk istniejących filmów

## Struktura bazy danych

Tabela `yt_movies` zawiera:
- `id` - unikalny identyfikator
- `video_id` - ID filmu YouTube
- `title` - tytuł filmu
- `playlist_id` - ID playlisty
- `playlist_title` - nazwa playlisty
- `view_count` - liczba wyświetleń
- `like_count` - liczba polubień
- `published_at` - data publikacji
- `created_at` - data dodania do bazy
- `updated_at` - data ostatniej aktualizacji

## Instalacja

1. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

2. Skonfiguruj zmienne środowiskowe:
```bash
cp env_example.txt .env
# Edytuj plik .env i ustaw swoje wartości
```

3. Utwórz bazę danych PostgreSQL i uruchom schema.sql:
```sql
CREATE DATABASE zero_stats;
\c zero_stats
\i schema.sql
```

## Konfiguracja

### Zmienne środowiskowe

- `DB_HOST` - host bazy danych (domyślnie: localhost)
- `DB_PORT` - port bazy danych (domyślnie: 5432)
- `DB_NAME` - nazwa bazy danych (domyślnie: zero_stats)
- `DB_USER` - użytkownik bazy danych
- `DB_PASSWORD` - hasło do bazy danych
- `YOUTUBE_API_KEY` - klucz API YouTube (wymagany)
- `CHANNEL_ID` - ID kanału YouTube do monitorowania
- `CHECK_INTERVAL_HOURS` - interwał sprawdzania nowych filmów (domyślnie: 6)
- `SKIP_PLAYLIST_IDS` - ID playlist do pominięcia (oddzielone przecinkami)

### YouTube API Key

Aby uzyskać klucz API YouTube:
1. Przejdź do [Google Cloud Console](https://console.cloud.google.com/)
2. Utwórz nowy projekt lub wybierz istniejący
3. Włącz YouTube Data API v3
4. Utwórz klucz API w sekcji Credentials

## Użycie

### Ładowanie początkowych danych
```bash
python -m app.data_loader.run_loader --initial
```

### Jednorazowe sprawdzenie nowych filmów
```bash
python -m app.data_loader.run_loader --check
```

### Ciągłe monitorowanie
```bash
python -m app.data_loader.run_loader --monitor
```

## Struktura plików

```
app/data_loader/
├── __init__.py
├── config.py          # Konfiguracja aplikacji
├── database.py        # Obsługa bazy danych
├── youtube_api.py     # Integracja z YouTube API
├── data_loader.py     # Główna logika aplikacji
├── run_loader.py      # Skrypt uruchamiający
├── schema.sql         # Definicja tabeli
├── requirements.txt   # Zależności Python
├── env_example.txt    # Przykład konfiguracji
└── README.md         # Ten plik
```

## Logi

Aplikacja zapisuje logi do pliku `data_loader.log` oraz wyświetla je w konsoli.

## Limity YouTube API

### Dzienne limity
- **Domyślny quota**: 10,000 jednostek dziennie
- **Można zwiększyć** do 100,000 jednostek dziennie (po weryfikacji)

### Koszty zapytań
- `playlists.list` - 1 jednostka
- `playlistItems.list` - 1 jednostka  
- `videos.list` - 1 jednostka (może zwrócić do 50 filmów)

### Dla kanału z 4700 filmami
- **Przed optymalizacją**: ~4795 jednostek (prawie połowa limitu)
- **Po optymalizacji**: ~100 jednostek (batch processing)

### Optymalizacje w aplikacji
- **Batch processing**: Pobieranie statystyk dla 50 filmów za jednym zapytaniem
- **Paginacja**: Automatyczne pobieranie wszystkich stron playlist
- **Opóźnienia**: Krótkie przerwy między zapytaniami
- **Filtrowanie playlist**: Możliwość pomijania określonych playlist po ID

## Przykład konfiguracji .env

```bash
# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password

# YouTube API configuration
YOUTUBE_API_KEY=your_youtube_api_key
CHANNEL_ID=UC_x5XG1OV2P6uZZ5FSM9Ttw

# Data loader configuration
CHECK_INTERVAL_HOURS=6

# Playlists to skip (comma-separated)
SKIP_PLAYLIST_IDS=PLvLrA9jH7wQhiFzfn5MfTn-zkR2DjtV6J,PLanother_playlist_id
```

## Uwagi

- YouTube API ma limity zapytań. Aplikacja zawiera opóźnienia między zapytaniami.
- Upewnij się, że masz wystarczające uprawnienia do bazy danych.
- Monitorowanie działa w pętli nieskończonej - użyj Ctrl+C aby zatrzymać.
- Dla dużych kanałów (>1000 filmów) zalecane jest zwiększenie quota w Google Cloud Console.
- Pomijane playlisty są logowane w konsoli i pliku logów. 