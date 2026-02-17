import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
}

# Schema configuration
DB_SCHEMA = os.getenv('DB_SCHEMA')
if not DB_SCHEMA:
    raise ValueError("DB_SCHEMA must be set (e.g. in .env)")
DB_TABLE = os.getenv('DB_TABLE')
if not DB_TABLE:
    raise ValueError("DB_TABLE must be set (e.g. in .env)")

# YouTube API configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = os.getenv('CHANNEL_ID', None)  # Google Developers as default

# Data loader configuration
CHECK_INTERVAL_HOURS = int(os.getenv('CHECK_INTERVAL_HOURS', '6'))  # Check every 6 hours by default
MAX_RESULTS_PER_REQUEST = 50  # YouTube API limit

# Playlists to skip (comma-separated IDs)
SKIP_PLAYLIST_IDS = os.getenv('SKIP_PLAYLIST_IDS', '').split(',') if os.getenv('SKIP_PLAYLIST_IDS') else []
# Remove empty strings and whitespace
SKIP_PLAYLIST_IDS = [pid.strip() for pid in SKIP_PLAYLIST_IDS if pid.strip()] 