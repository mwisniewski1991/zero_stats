#!/usr/bin/env python3
"""
Top playlists routes for displaying ranking table
"""

from flask import Blueprint, render_template, jsonify
from app.database import get_top_playlists

top_playlists = Blueprint('top_playlists', __name__, template_folder='templates', static_folder='static')

@top_playlists.route('/')
def top_playlists_index():
    """Top playlists ranking page"""
    try:
        playlists = get_top_playlists()
        return render_template('top_playlists.html', playlists=playlists)
    except Exception as e:
        return render_template('top_playlists.html', playlists=[], error=str(e))

@top_playlists.route('/api/data')
def top_playlists_data():
    """API endpoint for top playlists data (JSON)"""
    try:
        playlists = get_top_playlists()
        return jsonify({
            'playlists': [dict(playlist) for playlist in playlists]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 