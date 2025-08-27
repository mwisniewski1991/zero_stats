-- Schema for YouTube movies data
CREATE TABLE IF NOT EXISTS zero_stats.yt_movies (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    playlist_id VARCHAR(50) NOT NULL,
    playlist_title VARCHAR(200) NOT NULL,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_yt_movies_video_id ON zero_stats.yt_movies(video_id);
CREATE INDEX IF NOT EXISTS idx_yt_movies_playlist_id ON zero_stats.yt_movies(playlist_id);
CREATE INDEX IF NOT EXISTS idx_yt_movies_published_at ON zero_stats.yt_movies(published_at);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_yt_movies_updated_at 
    BEFORE UPDATE ON zero_stats.yt_movies 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 

    
CREATE TABLE zero_stats.agg_playlists_monthly (
    year_month VARCHAR(7) NOT NULL,
    playlist_id VARCHAR(255) NOT NULL,
    playlist_title TEXT NOT NULL,
    total_views BIGINT DEFAULT 0,
    total_likes BIGINT DEFAULT 0,
    total_videos INTEGER DEFAULT 0,
    
    PRIMARY KEY (year_month, playlist_id)
);

CREATE TABLE zero_stats.agg_playlists_summary (
    playlist_id VARCHAR(255) NOT NULL PRIMARY KEY,
    playlist_title TEXT NOT NULL,
    total_views BIGINT DEFAULT 0,
    total_likes BIGINT DEFAULT 0,
    total_videos INTEGER DEFAULT 0,
    avg_views DECIMAL(15,2) DEFAULT 0,
    avg_likes DECIMAL(15,2) DEFAULT 0
);