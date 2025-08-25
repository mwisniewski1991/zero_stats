from flask import Blueprint, render_template, jsonify
from app.database import get_playlists_monthly_data
from datetime import datetime
from collections import defaultdict

playlists_monthly = Blueprint('playlists_monthly', __name__, template_folder='templates', static_folder='static')

@playlists_monthly.route('/')
def playlists_monthly_index():
    try:
        monthly_data = get_playlists_monthly_data()
        
        # Generate complete month range from 2024.01 to current month
        current_date = datetime.now()
        current_month_str = f"{current_date.year}.{current_date.month:02d}"
        start_year, start_month = 2024, 1
        end_year, end_month = current_date.year, current_date.month
        
        # Create list of all months in range
        months_range = []
        year, month = start_year, start_month
        while year < end_year or (year == end_year and month <= end_month):
            months_range.append(f"{year}.{month:02d}")
            month += 1
            if month > 12:
                month = 1
                year += 1
        
        # Group data by playlist
        playlists = defaultdict(lambda: {
            'id': None,
            'title': None,
            'monthly_data': []
        })
        
        # First pass: collect existing data
        playlist_monthly_views = defaultdict(dict)
        playlist_monthly_likes = defaultdict(dict)
        playlist_monthly_counts = defaultdict(dict)
        
        for row in monthly_data:
            playlist_id = row['playlist_id']
            playlists[playlist_id]['id'] = playlist_id
            playlists[playlist_id]['title'] = row['playlist_title']
            playlist_monthly_views[playlist_id][row['year_month']] = row['total_views']
            playlist_monthly_likes[playlist_id][row['year_month']] = row['total_likes']
            playlist_monthly_counts[playlist_id][row['year_month']] = row['video_count']
        
        # Second pass: fill in complete data for each playlist
        for playlist_id in playlists:
            monthly_data_complete = []
            for month in months_range:
                views = playlist_monthly_views[playlist_id].get(month, 0)
                likes = playlist_monthly_likes[playlist_id].get(month, 0)
                count = playlist_monthly_counts[playlist_id].get(month, 0)
                monthly_data_complete.append({
                    'year_month': month,
                    'total_views': views,
                    'total_likes': likes,
                    'video_count': count
                })
            playlists[playlist_id]['monthly_data'] = monthly_data_complete
        
        return render_template('playlists_monthly.html', 
                             playlists=dict(playlists), 
                             current_month=current_month_str)
    except Exception as e:
        return render_template('playlists_monthly.html', 
                             playlists={}, 
                             error=str(e),
                             current_month="")