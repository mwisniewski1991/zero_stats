import requests
import logging
import time
from typing import List, Dict, Optional
from datetime import datetime
from .config import YOUTUBE_API_KEY, CHANNEL_ID, MAX_RESULTS_PER_REQUEST, SKIP_PLAYLIST_IDS

logger = logging.getLogger(__name__)

class YouTubeAPIManager:
    def __init__(self, api_key: str | None = None, channel_id: str | None = None):
        self.api_key = api_key or YOUTUBE_API_KEY
        self.channel_id = channel_id or CHANNEL_ID
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
        if not self.api_key:
            raise ValueError("YouTube API key is required")
            
    def get_channel_playlists(self) -> List[Dict]:
        """Pobiera wszystkie playlisty kanału (z pomijaniem określonych ID i paginacją)"""
        playlists = []
        skipped_count = 0
        next_page_token = None
        
        while True:
            url = f"{self.base_url}/playlists"
            params = {
                'part': 'snippet',
                'channelId': self.channel_id,
                'key': self.api_key,
                'maxResults': MAX_RESULTS_PER_REQUEST
            }
            
            if next_page_token:
                params['pageToken'] = next_page_token
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                for item in data.get('items', []):
                    playlist_id = item['id']
                    
                    # Sprawdź czy playlistę należy pominąć
                    if playlist_id in SKIP_PLAYLIST_IDS:
                        logger.info(f"Pominięto playlistę: {item['snippet']['title']} (ID: {playlist_id})")
                        skipped_count += 1
                        continue
                    
                    playlist = {
                        'id': playlist_id,
                        'title': item['snippet']['title'],
                        'description': item['snippet'].get('description', ''),
                        'video_count': item['snippet'].get('videoCount', 0),
                        'published_at': item['snippet'].get('publishedAt')
                    }
                    playlists.append(playlist)
                
                # Sprawdź czy są kolejne strony
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    break
                    
                # Krótka przerwa między stronami
                time.sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Błąd przy pobieraniu playlist: {e}")
                break
                
        logger.info(f"Pobrano {len(playlists)} playlist z kanału (pominięto {skipped_count})")
        return playlists
            
    def get_playlist_videos(self, playlist_id: str) -> List[Dict]:
        """Pobiera wszystkie filmy z playlisty (z paginacją)"""
        videos = []
        next_page_token = None
        
        while True:
            url = f"{self.base_url}/playlistItems"
            params = {
                'part': 'snippet',
                'playlistId': playlist_id,
                'key': self.api_key,
                'maxResults': MAX_RESULTS_PER_REQUEST
            }
            
            if next_page_token:
                params['pageToken'] = next_page_token
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                for item in data.get('items', []):
                    video_id = item['snippet']['resourceId']['videoId']
                    video = {
                        'video_id': video_id,
                        'title': item['snippet']['title'],
                        'description': item['snippet'].get('description', ''),
                        'published_at': item['snippet'].get('publishedAt'),
                        'playlist_id': playlist_id
                    }
                    videos.append(video)
                
                # Sprawdź czy są kolejne strony
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    break
                    
                # Krótka przerwa między stronami
                time.sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Błąd przy pobieraniu filmów z playlisty {playlist_id}: {e}")
                break
                
        logger.info(f"Pobrano {len(videos)} filmów z playlisty {playlist_id}")
        return videos
            
    def get_video_stats(self, video_id: str) -> Optional[Dict]:
        """Pobiera statystyki filmu (wyświetlenia, polubienia)"""
        url = f"{self.base_url}/videos"
        params = {
            'part': 'statistics,snippet',
            'id': video_id,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('items'):
                logger.warning(f"Nie znaleziono filmu: {video_id}")
                return None
                
            item = data['items'][0]
            stats = item.get('statistics', {})
            
            video_stats = {
                'video_id': video_id,
                'title': item['snippet']['title'],
                'view_count': int(stats.get('viewCount', 0)),
                'like_count': int(stats.get('likeCount', 0)),
                'comment_count': int(stats.get('commentCount', 0)),
                'published_at': item['snippet'].get('publishedAt')
            }
            
            return video_stats
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Błąd przy pobieraniu statystyk filmu {video_id}: {e}")
            return None
            
    def get_all_videos_with_stats(self, playlist_id: str, playlist_title: str) -> List[Dict]:
        """Pobiera wszystkie filmy z playlisty wraz ze statystykami"""
        videos = self.get_playlist_videos(playlist_id)
        if not videos:
            return []
            
        # Pobierz wszystkie video_id
        video_ids = [video['video_id'] for video in videos]
        
        # Pobierz statystyki dla wszystkich filmów za jednym razem
        all_stats = self.get_videos_stats_batch(video_ids)
        
        videos_with_stats = []
        for video in videos:
            video_id = video['video_id']
            stats = all_stats.get(video_id)
            
            if stats:
                video_data = {
                    'video_id': video_id,
                    'title': video['title'],
                    'playlist_id': playlist_id,
                    'playlist_title': playlist_title,
                    'view_count': stats['view_count'],
                    'like_count': stats['like_count'],
                    'published_at': video['published_at']
                }
                videos_with_stats.append(video_data)
                
        logger.info(f"Pobrano statystyki dla {len(videos_with_stats)} filmów z playlisty {playlist_title}")
        return videos_with_stats
        
    def get_videos_stats_batch(self, video_ids: List[str]) -> Dict[str, Dict]:
        """Pobiera statystyki dla wielu filmów za jednym razem (oszczędza quota)"""
        if not video_ids:
            return {}
            
        # YouTube API pozwala na max 50 filmów na zapytanie
        batch_size = 50
        all_stats = {}
        
        for i in range(0, len(video_ids), batch_size):
            batch_ids = video_ids[i:i + batch_size]
            batch_stats = self._get_videos_stats_single_batch(batch_ids)
            all_stats.update(batch_stats)
            
            # Krótka przerwa między batchami
            if i + batch_size < len(video_ids):
                time.sleep(0.1)
                
        return all_stats
        
    def _get_videos_stats_single_batch(self, video_ids: List[str]) -> Dict[str, Dict]:
        """Pobiera statystyki dla jednej partii filmów (max 50)"""
        url = f"{self.base_url}/videos"
        params = {
            'part': 'statistics,snippet',
            'id': ','.join(video_ids),
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            stats_dict = {}
            for item in data.get('items', []):
                video_id = item['id']
                stats = item.get('statistics', {})
                
                stats_dict[video_id] = {
                    'video_id': video_id,
                    'title': item['snippet']['title'],
                    'view_count': int(stats.get('viewCount', 0)),
                    'like_count': int(stats.get('likeCount', 0)),
                    'comment_count': int(stats.get('commentCount', 0)),
                    'published_at': item['snippet'].get('publishedAt')
                }
                
            return stats_dict
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Błąd przy pobieraniu statystyk dla batch: {e}")
            return {}
            
    def check_quota_usage(self) -> Dict:
        """Sprawdza użycie quota API (wymaga dodatkowych uprawnień)"""
        # To jest opcjonalne - wymaga dodatkowych uprawnień w Google Cloud Console
        try:
            # Można dodać sprawdzanie quota przez Google Cloud Console API
            # Na razie zwracamy podstawowe informacje
            return {
                'quota_available': True,
                'message': 'Quota checking requires additional API permissions'
            }
        except Exception as e:
            logger.warning(f"Nie można sprawdzić quota: {e}")
            return {'quota_available': True, 'message': 'Quota check failed'} 