from flask import Blueprint, render_template, jsonify
from app.database import get_playlists_data

playlists = Blueprint('playlists', __name__, template_folder='templates', static_folder='static')

@playlists.route('/')
def playlists_index():
    """Playlists overview page"""
    try:
        playlists_data = get_playlists_data()
        
        # Group data by playlist
        playlists = {}
        for row in playlists_data:
            playlist_id = row['playlist_id']
            if playlist_id not in playlists:
                playlists[playlist_id] = {
                    'id': playlist_id,
                    'title': row['playlist_title'],
                    'videos': []
                }
            
            playlists[playlist_id]['videos'].append({
                'video_id': row['video_id'],
                'title': row['title'],
                'view_count': row['view_count'],
                'like_count': row['like_count'],
                'published_at': row['published_at'].isoformat() if row['published_at'] else None
            })
        
        # Sort videos in each playlist by published_at ASC
        for playlist in playlists.values():
            playlist['videos'].sort(key=lambda v: v['published_at'] or '')
            # Top 5 videos by view_count
            playlist['top_videos'] = sorted(playlist['videos'], key=lambda v: v['view_count'], reverse=True)[:5]
        
        return render_template('playlists.html', playlists=playlists)
    except Exception as e:
        return render_template('playlists.html', playlists={}, error=str(e))
