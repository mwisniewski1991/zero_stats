from flask import Blueprint, render_template, jsonify
from app.database import get_playlists_monthly_data
from collections import defaultdict

playlists_monthly = Blueprint('playlists_monthly', __name__, template_folder='templates', static_folder='static')

@playlists_monthly.route('/')
def playlists_monthly_index():
    try:
        monthly_data = get_playlists_monthly_data()
        
        # Group data by playlist - much simpler since data is already complete
        playlists = defaultdict(lambda: {
            'id': None,
            'title': None,
            'monthly_data': []
        })
        
        for row in monthly_data:
            playlist_id = row['playlist_id']
            playlists[playlist_id]['id'] = playlist_id
            playlists[playlist_id]['title'] = row['playlist_title']
            playlists[playlist_id]['monthly_data'].append({
                'year_month': row['year_month'],
                'total_views': row['total_views'],
                'total_likes': row['total_likes'],
                'video_count': row['video_count']
            })
        
        return render_template('playlists_monthly.html', 
                             playlists=dict(playlists))
    except Exception as e:
        return render_template('playlists_monthly.html', 
                             playlists={}, 
                             error=str(e))