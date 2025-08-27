from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
import jinja2

@dag(
    dag_id='zero_stats_agg_playlists_monthly_PROD',
    description='Agregacja danych o playlistach',
    start_date=datetime(2025, 8, 21),
    schedule='0 2 * * *',
    catchup=False,
    max_active_runs=3,
    tags=['zero_stats','PROD'],
    default_args={
        'owner': 'mateuszwisniewski',
    }
)
def zero_stats_agg_playlists_monthly(**context):
    """DAG do agregacji danych o playlistach"""
    
    # Task 1: Agregacja danych
    @task(task_id='aggregate_playlists_data')
    def aggregate_playlists_data(**context):
        """Agreguje dane o playlistach"""
        hook = PostgresHook(postgres_conn_id='mikrus_postgres_PROD_zero_stats_writer')
        
        # Odczytaj SQL z pliku
        sql = jinja2.Template(
            open('queries/zero_stats/agg_playlists_monthly.sql', 'r').read()
        )
        # Wykonaj zapytanie z parametrem timestamp
        hook.run(sql.render())
    
    aggregate_data = aggregate_playlists_data()
    # validate_data = validate_data_quality()

zero_stats_agg_playlists_monthly()