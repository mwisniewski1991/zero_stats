# #!/usr/bin/env python3
# """
# Summary route for displaying global statistics
# """

# from flask import Blueprint, render_template
# from database import get_playlist_summary

# summary_bp = Blueprint('summary', __name__)

# @summary_bp.route('/')
# def summary_index():
#     try:
#         summary = get_playlist_summary()
#     except Exception as e:
#         summary = {
#             'total_playlists': 0,
#             'total_videos': 0,
#             'total_views': 0,
#             'total_likes': 0
#         }
#     return render_template('summary.html', summary=summary) 