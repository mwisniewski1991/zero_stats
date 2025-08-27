INSERT INTO zero_stats.agg_playlists_monthly (year_month, playlist_id, playlist_title, total_views, total_likes, total_videos)
WITH years_months AS ( 
	SELECT to_char(date_trunc('month', generate_series(
	    '2024-01-01'::date, 
	     (now() - INTERVAL '1 day')::date, 
	    '1 month'::interval
	)), 'YYYY.MM') AS year_month
)
,distinct_playlits as (
	select 
		ym.playlist_id, MAX(ym.playlist_title) as playlist_title
	from zero_stats.yt_movies ym 
	WHERE ym.published_at::date <= (now() - INTERVAL '1 day')::date
	group by ym.playlist_id
)
,crossed_data as (
	select year_month, playlist_id, playlist_title 
	from years_months
	cross join distinct_playlits
)
,playlists_agg as (
	select 
		to_char(ym.published_at, 'YYYY.MM') as year_month,
		ym.playlist_id, 
		MAX(ym.playlist_title) as playlist_title, 
		sum(ym.view_count) as total_views, 
		sum(ym.like_count) as total_likes,
		count(ym.video_id) as total_videos
	from zero_stats.yt_movies ym 
	WHERE ym.published_at::date <= (now() - INTERVAL '1 day')::date
	group by ym.playlist_id, to_char(ym.published_at, 'YYYY.MM')
)
,crossed_agg as (
	select
		cd.year_month,
		cd.playlist_id, cd.playlist_title, 
		coalesce(agg.total_views,0) as total_views, 
		coalesce(agg.total_likes,0) as total_likes,
		coalesce(agg.total_videos,0) as total_videos
	from crossed_data as cd
	left join playlists_agg as agg
		on cd.year_month = agg.year_month
		and cd.playlist_id  = agg.playlist_id
)
select * 
from crossed_agg
ON CONFLICT (year_month, playlist_id) 
DO UPDATE SET 
    playlist_title = EXCLUDED.playlist_title,
    total_views = EXCLUDED.total_views,
    total_likes = EXCLUDED.total_likes,
    total_videos = EXCLUDED.total_videos;
