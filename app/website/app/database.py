#!/usr/bin/env python3
"""
Database connection and query utilities for the web application
"""

import psycopg2
import psycopg2.extras
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    """Get database connection using Flask app config"""
    try:
        conn = psycopg2.connect(
            host=current_app.config['DB_CONFIG']['host'],
            port=current_app.config['DB_CONFIG']['port'],
            database=current_app.config['DB_CONFIG']['database'],
            user=current_app.config['DB_CONFIG']['user'],
            password=current_app.config['DB_CONFIG']['password']
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def get_playlists_data():
    """Get all playlists with their videos and statistics"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            schema = current_app.config['DB_SCHEMA']
            cur.execute(f"""
                SELECT 
                    playlist_id,
                    playlist_title,
                    video_id,
                    title,
                    view_count,
                    like_count,
                    published_at
                FROM {schema}.yt_movies
                ORDER BY playlist_title, view_count DESC
            """)
            return cur.fetchall()
    finally:
        conn.close()


def get_top_playlists():
    """Get playlists ranked by total views"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            schema = current_app.config['DB_SCHEMA']
            cur.execute(f"""
                SELECT 
                    playlist_id,
                    playlist_title,
                    total_views,
                    total_likes,
                    total_videos,
                    avg_views,
                    avg_likes
                FROM {schema}.agg_playlists_summary
                ORDER BY total_views DESC
            """)
            return cur.fetchall()
    finally:
        conn.close()



def get_playlists_monthly_data():
    """Get playlists data aggregated by month and year from agg_playlists_monthly table"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            schema = current_app.config['DB_SCHEMA']
            cur.execute(f"""
                SELECT 
                    playlist_id,
                    playlist_title,
                    year_month,
                    total_views,
                    total_likes,
                    total_videos as video_count
                FROM {schema}.agg_playlists_monthly
                ORDER BY playlist_title, year_month
            """)
            return cur.fetchall()
    finally:
        conn.close() 