import logging
from .database import DatabaseManager
from .youtube_api import YouTubeAPIManager
from typing import List, Dict
import time
from .config import CHECK_INTERVAL_HOURS


# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_loader.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.youtube_api = YouTubeAPIManager()
        
    def initialize_database(self):
        """Inicjalizuje połączenie z bazą danych"""
        try:
            self.db_manager.connect()
            logger.info("Baza danych zainicjalizowana")
        except Exception as e:
            logger.error(f"Błąd inicjalizacji bazy danych: {e}")
            raise
            
    def load_initial_data(self):
        """Ładuje początkowe dane - wszystkie playlisty i filmy"""
        logger.info("Rozpoczynam ładowanie początkowych danych...")
        
        try:
            # Pobierz wszystkie playlisty
            playlists = self.youtube_api.get_channel_playlists()
            
            if not playlists:
                logger.warning("Nie znaleziono żadnych playlist")
                return
                
            total_videos_processed = 0
            total_playlists = len(playlists)
            
            logger.info(f"Znaleziono {total_playlists} playlist do przetworzenia")
            
            for i, playlist in enumerate(playlists, 1):
                logger.info(f"Przetwarzam playlistę {i}/{total_playlists}: {playlist['title']} ({playlist['video_count']} filmów)")
                
                # Pobierz filmy z playlisty wraz ze statystykami
                videos = self.youtube_api.get_all_videos_with_stats(
                    playlist['id'], 
                    playlist['title']
                )
                
                # Zapisz filmy do bazy danych
                videos_added = self._save_videos_to_database(videos)
                total_videos_processed += videos_added
                
                logger.info(f"✓ Playlista {i}/{total_playlists} - dodano {videos_added} filmów")
                
                # Krótka przerwa między playlistami aby nie przekroczyć limitów API
                time.sleep(1)
                
            logger.info(f"Zakończono ładowanie początkowych danych. Dodano {total_videos_processed} filmów z {total_playlists} playlist.")
        except Exception as e:
            logger.error(f"Błąd podczas ładowania początkowych danych: {e}")
            raise
            
    def check_for_new_videos(self):
        """Sprawdza czy pojawiły się nowe filmy i aktualizuje statystyki"""
        logger.info("Sprawdzam nowe filmy i aktualizuję statystyki...")
        
        try:
            # Pobierz wszystkie playlisty
            playlists = self.youtube_api.get_channel_playlists()
            
            new_videos_count = 0
            updated_videos_count = 0
            new_playlists_count = 0
            
            for playlist in playlists:
                # Sprawdź czy playlista istnieje w bazie
                if not self.db_manager.playlist_exists(playlist['id']):
                    logger.info(f"Znaleziono nową playlistę: {playlist['title']}")
                    new_playlists_count += 1
                
                logger.info(f"Sprawdzam playlistę: {playlist['title']}")
                
                # Pobierz filmy z playlisty wraz ze statystykami
                videos = self.youtube_api.get_all_videos_with_stats(
                    playlist['id'], 
                    playlist['title']
                )
                
                for video in videos:
                    if self.db_manager.video_exists(video['video_id']):
                        # Film już istnieje - zaktualizuj statystyki
                        self.db_manager.update_video_stats(
                            video['video_id'],
                            video['view_count'],
                            video['like_count']
                        )
                        updated_videos_count += 1
                    else:
                        # Nowy film - dodaj do bazy (automatycznie dodaje info o playliście)
                        self.db_manager.insert_video(video)
                        new_videos_count += 1
                        logger.info(f"Dodano nowy film: {video['title']}")
                
                # Krótka przerwa między playlistami
                time.sleep(1)
                
            logger.info(f"Sprawdzanie zakończone. Nowe playlisty: {new_playlists_count}, Nowe filmy: {new_videos_count}, Zaktualizowane: {updated_videos_count}")
            
        except Exception as e:
            logger.error(f"Błąd podczas sprawdzania nowych filmów: {e}")
            raise
            
    def _save_videos_to_database(self, videos: List[Dict]) -> int:
        """Zapisuje filmy do bazy danych, zwraca liczbę dodanych filmów"""
        added_count = 0
        
        for video in videos:
            try:
                if not self.db_manager.video_exists(video['video_id']):
                    self.db_manager.insert_video(video)
                    added_count += 1
                else:
                    logger.debug(f"Film już istnieje w bazie: {video['title']}")
            except Exception as e:
                logger.error(f"Błąd podczas zapisywania filmu {video['video_id']}: {e}")
                
        return added_count

    def cleanup(self):
        """Zamyka połączenia"""
        self.db_manager.disconnect()
        logger.info("Zakończono pracę DataLoader") 