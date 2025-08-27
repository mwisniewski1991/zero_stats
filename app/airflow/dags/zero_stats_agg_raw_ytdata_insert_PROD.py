from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from zero_stats.prod.utils.data_loader import DataLoader
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create DAG
@dag(
    dag_id='zero_stats_agg_raw_ytdata_insert_PROD',
    description='Check for new videos and update statistics',
    start_date=datetime(2025, 8, 21),
    schedule='0 1 * * *',
    catchup=False,
    max_active_runs=1,
    tags=['zero_stats','PROD'],  
    default_args={
        'owner': 'mateuszwisniewski',
    }
)
def zero_stats_check_new_videos_dev():
    """DAG do sprawdzania nowych filmów i aktualizacji statystyk"""

    # Task 1: Sprawdzenie nowych filmów
    @task(task_id='check_for_new_videos')
    def check_for_new_videos():
        """Sprawdza czy pojawiły się nowe filmy i aktualizuje statystyki"""
        logger.info("Sprawdzam nowe filmy i aktualizuję statystyki...")

        # Inicjalizacja DataLoader
        data_loader = DataLoader()

        # Inicjalizacja połączenia z bazą danych
        data_loader.initialize_database()

        # Sprawdzenie nowych filmów i aktualizacja statystyk
        data_loader.check_for_new_videos()

        logger.info("Sprawdzenie nowych filmów i aktualizacja statystyk zakończone")

    check_for_new_videos()

# Task dependencies (single task in this case)
zero_stats_check_new_videos_dev()
