{{
  config(
    materialized='table',
    unique_key='playlist_id'
  )
}}

SELECT 
    playlist_id,
    MAX(playlist_title) as playlist_title,
    SUM(view_count) as total_views,
    SUM(like_count) as total_likes,
    COUNT(*) as total_videos,
    AVG(view_count) as avg_views,
    AVG(like_count) as avg_likes
FROM {{ source('zero_stats', 'yt_movies') }}
WHERE published_at::date <= CURRENT_DATE - INTERVAL '1 day'
GROUP BY playlist_id
ORDER BY total_views DESC
