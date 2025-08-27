INSERT INTO zero_stats.agg_playlists_summary (playlist_id, playlist_title, total_views, total_likes, total_videos, avg_views, avg_likes)
SELECT 
    playlist_id,
    MAX(playlist_title) as playlist_title,
    SUM(view_count) as total_views,
    SUM(like_count) as total_likes,
    COUNT(*) as total_videos,
    AVG(view_count) as avg_views,
    AVG(like_count) as avg_likes
FROM zero_stats.yt_movies
WHERE published_at::date <= CURRENT_DATE - INTERVAL '1 day'
GROUP BY playlist_id
ORDER BY total_views DESC
ON CONFLICT (playlist_id) 
DO UPDATE SET 
    playlist_title = EXCLUDED.playlist_title,
    total_views = EXCLUDED.total_views,
    total_likes = EXCLUDED.total_likes,
    total_videos = EXCLUDED.total_videos,
    avg_views = EXCLUDED.avg_views,
    avg_likes = EXCLUDED.avg_likes;