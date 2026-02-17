import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional
import logging
from .config import DB_CONFIG, DB_SCHEMA, DB_TABLE

# Quoted identifier for tables/schemas that start with digits (e.g. 03_bronze_yt_movies)
QUALIFIED_TABLE = f'"{DB_SCHEMA}"."{DB_TABLE}"'

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection: psycopg2.extensions.connection | None = None
        
    def connect(self):
        """Nawiązuje połączenie z bazą danych"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            logger.info("Połączenie z bazą danych nawiązane")
        except Exception as e:
            logger.error(f"Błąd połączenia z bazą danych: {e}")
            raise
            
    def disconnect(self):
        """Zamyka połączenie z bazą danych"""
        if self.connection:
            self.connection.close()
            logger.info("Połączenie z bazą danych zamknięte")
            
    def execute_query(self, query: str, params: tuple | None = None):
        """Wykonuje zapytanie SQL"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Błąd wykonania zapytania: {e}")
            raise
            
    def fetch_all(self, query: str, params: tuple | None = None) -> List[Dict]:
        """Pobiera wszystkie wyniki zapytania"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Błąd pobierania danych: {e}")
            raise
            
    def fetch_one(self, query: str, params: tuple | None = None) -> Optional[Dict]:
        """Pobiera jeden wynik zapytania"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Błąd pobierania danych: {e}")
            raise
            
    def video_exists(self, video_id: str) -> bool:
        """Sprawdza czy film już istnieje w bazie"""
        query = f"SELECT 1 FROM {QUALIFIED_TABLE} WHERE video_id = %s"
        result = self.fetch_one(query, (video_id,))
        return result is not None
        
    def insert_video(self, video_data: Dict):
        """Dodaje nowy film do bazy danych"""
        query = f"""
        INSERT INTO {QUALIFIED_TABLE} (video_id, title, playlist_id, playlist_title, 
                              view_count, like_count, published_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            video_data['video_id'],
            video_data['title'],
            video_data['playlist_id'],
            video_data['playlist_title'],
            video_data['view_count'],
            video_data['like_count'],
            video_data['published_at']
        )
        self.execute_query(query, params)
        logger.info(f"Dodano film: {video_data['title']}")
        
    def update_video_stats(self, video_id: str, view_count: int, like_count: int):
        """Aktualizuje statystyki filmu"""
        query = f"""
        UPDATE {QUALIFIED_TABLE} 
        SET view_count = %s, like_count = %s 
        WHERE video_id = %s
        """
        self.execute_query(query, (view_count, like_count, video_id))
        logger.info(f"Zaktualizowano statystyki filmu: {video_id}")
        
    def get_all_videos(self) -> List[Dict]:
        """Pobiera wszystkie filmy z bazy"""
        query = f"SELECT * FROM {QUALIFIED_TABLE} ORDER BY published_at DESC"
        return self.fetch_all(query)
        
    def get_videos_by_playlist(self, playlist_id: str) -> List[Dict]:
        """Pobiera filmy z konkretnej playlisty"""
        query = f"SELECT * FROM {QUALIFIED_TABLE} WHERE playlist_id = %s ORDER BY published_at DESC"
        return self.fetch_all(query, (playlist_id,)) 

    def playlist_exists(self, playlist_id: str) -> bool:
        """Sprawdza czy playlista już istnieje w bazie"""
        query = f"SELECT 1 FROM {QUALIFIED_TABLE} WHERE playlist_id = %s LIMIT 1"
        result = self.fetch_one(query, (playlist_id,))
        return result is not None
        
    def get_existing_playlists(self) -> List[str]:
        """Pobiera listę ID wszystkich playlist w bazie"""
        query = f"SELECT DISTINCT playlist_id FROM {QUALIFIED_TABLE}"
        results = self.fetch_all(query)
        return [row['playlist_id'] for row in results] 