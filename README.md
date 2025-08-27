# YouTube Statistics Dashboard


## 📑 Table of Contents
- [🛠️ Technologies](#️-technologies)
- [🔄 Process Overview](#-process-overview)
- [📋 Process Details](#-process-details)
    - [📡 Sources](#-sources)
    - [🐘 PostgreSQL](#-postgresql)
    - [⚙️ Data processing and orchestration](#️-data-processing-and-orchestration)
    - [📊 Dashboard](#-dashboard)

## 🛠️ Technologies
- **Backend+Frontend:** 🐍 Flask,  🌐 nginx (reverse proxy), 📊 D3.js
- **Database:** 🐘 PostgreSQL
- **Orchestration:** 🔄 Apache Airflow
- **Deployment:** 🐳 Docker Compose
- **Hosting:** ☁️ mikr.us
- **Data Collection:** 🐍Python, 🤖YouTube API


## 🔄 Process Overview
![Process overview](readme_utils/process_overview.png)

## 📋 Process Details

### 📡 Sources
Youtube API

**Data collection process:**
- 🔍 **Playlist discovery** - fetching all playlists from the YouTube channel
- 📹 **Video cataloging** - collecting videos from each playlist
- 📊 **Statistics retrieval** - views, likes, publication dates
- 💾 **Database storage** - saving data in the `yt_movies` table
- 🔄 **Update** - periodically refreshing statistics of existing videos
- ⚡ **Optimization** - batch processing (50 videos per request) to save API quota

### 🐘 PostgreSQL
Tables:
- yt_movies
- agg_playlists_summary
- agg_playlists_monthly

SQL Scripts
- 📂[DDL](https://github.com/mwisniewski1991/zero_stats/tree/master/app/database_definitions/ddl)
- 📂[Aggregations](https://github.com/mwisniewski1991/zero_stats/tree/master/app/database_definitions/aggregations)

### ⚙️ Data processing and orchestration
![Data Flow](readme_utils/data_flow.png)

🔄 Calculations are performed at the database level and are run using the Airflow application (it is hosted on my home Homelab).
![Airflow DAGs](readme_utils/airflow_dags.png)

DAGs are ver simple and launch calculation on Database server.
📂 [Link to DAGs directory](https://github.com/mwisniewski1991/iot_personal_hub/tree/master/app/airflow)

dags list:
- zero_stats_agg_raw_ytdata_insert_PROD - fetches data from the API
- zero_stats_agg_playlists_summary_PROD - creates aggregate playlist summary
- zero_stats_agg_playlists_monthly_PROD - creates monthly playlist summary


### 📊 Dashboard

**Dostępne wizualizacje:**

- **📊 Filmy w Playlistach** - Interaktywne wykresy słupkowe dla każdej playlisty pokazujące wyświetlenia poszczególnych filmów.
  - Tooltipami z dokładnymi wartościami i tytułami filmów
  - Linią średniej wyświetleń (przerywana)


- **📊 Playlisty Miesięczne** - Wykresy słupkowe przedstawiające miesięczne statystyki playlist od stycznia 2024:
  - Suma wyświetleń per miesiąc dla każdej playlisty
  - Liczba filmów w każdym miesiącu
  - Linią średniej wyświetleń

- **🏆 Ranking Playlist** - Interaktywna tabela DataTables z:
  - Statystykami: łączne wyświetlenia, polubienia, średnie wartości
  - Sortowaniem według łącznych wyświetleń (domyślnie)

**Technologia wizualizacji:** D3.js v7 z responsywnym designem i ciemnym motywem

